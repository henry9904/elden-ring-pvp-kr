r"""
Verify (and optionally confirm) the glossary against the game's own text files.

    python glossary/tools/game_text.py --game "H:\SteamLibrary\steamapps\common\ELDEN RING\Game"
    python glossary/tools/game_text.py --game "..." --apply   # rows that match exactly -> source game-text, status ok

Needs (local only, never in CI):
  - Windows, the installed game (oo2core_6_win64.dll is used for Oodle/KRAK decompression)
  - msg/korKR and msg/engUS unpacked with UXM Selective Unpack (unpack only, do NOT patch the exe)
Reads only; writes nothing to the game folder. Only names and short menu terms are compared,
descriptions/dialogue are never stored.

Matching rules:
  - items: WeaponName / ProtectorName / AccessoryName / GoodsName (+ _dlc01, _dlc02), by game id
  - terms: GR_MenuText. English is matched case-insensitively; armor parts use the menu labels
    (Head/Chest/Arms/Legs) because the game does not use the words in inputs/terms.csv
"""
import argparse
import csv
import ctypes
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_glossary as cg  # noqa: E402

GAME = Path(r"C:\Program Files (x86)\Steam\steamapps\common\ELDEN RING\Game")
_oodle = None


def oodle():
    global _oodle
    if _oodle is None:
        _oodle = ctypes.WinDLL(str(GAME / "oo2core_6_win64.dll"))
        f = _oodle.OodleLZ_Decompress
        f.restype = ctypes.c_int64
        f.argtypes = [ctypes.c_void_p, ctypes.c_int64, ctypes.c_void_p, ctypes.c_int64,
                      ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_int64,
                      ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int64, ctypes.c_int]
    return _oodle


def read_dcx(buf: bytes) -> bytes:
    assert buf[:4] == b"DCX\0", "not DCX"
    kind = buf[0x28:0x2C]
    raw_size, comp_size = struct.unpack(">II", buf[0x1C:0x24])
    dca = buf.index(b"DCA\0", 0x2C)
    data_at = dca + struct.unpack(">I", buf[dca + 4:dca + 8])[0]
    comp = buf[data_at:data_at + comp_size]
    if kind == b"KRAK":
        out = ctypes.create_string_buffer(raw_size)
        n = oodle().OodleLZ_Decompress(comp, len(comp), out, raw_size, 1, 0, 0, None, 0, None, None, None, 0, 3)
        assert n == raw_size, f"oodle returned {n}, expected {raw_size}"
        return out.raw
    if kind == b"DFLT":
        import zlib
        return zlib.decompress(comp)
    raise ValueError(f"unsupported DCX {kind!r}")


def _rev(b):
    return int(f"{b:08b}"[::-1], 2)


def read_bnd4(buf: bytes) -> dict:
    assert buf[:4] == b"BND4"
    bit_big = buf[0x0A] == 0
    count = struct.unpack_from("<i", buf, 0x0C)[0]
    hsize = struct.unpack_from("<q", buf, 0x20)[0]
    unicode = buf[0x30] == 1
    raw = buf[0x31]
    fmt = raw if (bit_big or (raw & 1 and not raw & 0x80)) else _rev(raw)
    files = {}
    for i in range(count):
        p = 0x40 + i * hsize + 8
        size = struct.unpack_from("<q", buf, p)[0]; p += 8
        if fmt & 0x20: p += 8
        if fmt & 0x10:
            off = struct.unpack_from("<q", buf, p)[0]; p += 8
        else:
            off = struct.unpack_from("<I", buf, p)[0]; p += 4
        if fmt & 0x02: p += 4
        name_at = struct.unpack_from("<I", buf, p)[0]
        end = name_at
        if unicode:
            while buf[end:end + 2] != b"\0\0": end += 2
            name = buf[name_at:end].decode("utf-16le")
        else:
            while buf[end] != 0: end += 1
            name = buf[name_at:end].decode("latin1")
        files[name.replace("\\", "/").split("/")[-1]] = buf[off:off + size]
    return files


def read_fmg(buf: bytes) -> dict:
    """FMG (version 2, little endian) -> {id: text}. Same layout as 신님's scripts/fmg.mjs."""
    assert buf[0] == 0 and buf[1] == 0
    groups = struct.unpack_from("<i", buf, 0x0C)[0]
    offsets_at = struct.unpack_from("<q", buf, 0x18)[0]
    pos, out = 0x28, {}
    for _ in range(groups):
        idx, first, last = struct.unpack_from("<iii", buf, pos); pos += 16
        for j in range(last - first + 1):
            s = struct.unpack_from("<q", buf, offsets_at + (idx + j) * 8)[0]
            if not s: continue
            e = s
            while buf[e:e + 2] != b"\0\0": e += 2
            t = buf[s:e].decode("utf-16le").strip()
            if t: out[first + j] = t
    return out


def load(lang: str, bundle: str) -> dict:  # noqa: D401
    """{fmg file name: {id: text}} for msg/<lang>/<bundle>.msgbnd.dcx"""
    files = read_bnd4(read_dcx((GAME / "msg" / lang / f"{bundle}.msgbnd.dcx").read_bytes()))
    return {name: read_fmg(data) for name, data in files.items() if name.endswith(".fmg")}




ITEM_FMG = {"weapons": "WeaponName", "armor": "ProtectorName", "talismans": "AccessoryName", "goods": "GoodsName"}
# inputs/terms.csv English -> how the game menu writes it
TERM_EN_ALIASES = {"Helm": "Head", "Chest Armor": "Chest", "Gauntlets": "Arms", "Leg Armor": "Legs"}
SKIP_MENU = ("Caption", "Info", "Dialog", "Talk", "Subtitle", "Loading", "BloodMsg")


def merged(fmgs: dict, prefix: str) -> dict:
    out = {}
    for name in sorted(n for n in fmgs if n == f"{prefix}.fmg" or (n.startswith(f"{prefix}_dlc") and n.endswith(".fmg"))):
        out.update(fmgs[name])
    return out


def menu_terms(en_menu: dict, ko_menu: dict) -> dict:
    """lower-case English menu text -> set of Korean texts with the same id (GR_MenuText only)"""
    out = {}
    for name, en in en_menu.items():
        if not name.startswith("GR_MenuText") or any(s in name for s in SKIP_MENU):
            continue
        ko = ko_menu.get(name, {})
        for i, e in en.items():
            if i in ko:
                out.setdefault(e.strip().lower(), set()).add(ko[i])
    return out


def main(argv=None):
    cg.ensure_utf8_stdout()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--game", type=Path, default=None, help=r"ELDEN RING\Game folder (default: Steam default path)")
    ap.add_argument("--apply", action="store_true", help="exact matches -> source game-text, status ok")
    args = ap.parse_args(argv)
    global GAME
    if args.game is not None:
        GAME = args.game

    ko_item, en_item = load("korkr", "item_dlc02"), load("engus", "item_dlc02")
    terms_index = menu_terms(load("engus", "menu_dlc02"), load("korkr", "menu_dlc02"))
    note = "게임 텍스트(msg/korKR·engUS) 직접 대조 일치"
    exit_code = 0
    for category in cg.CATEGORIES:
        path = cg.OUTPUT_DIR / f"{category}.csv"
        _, rows = cg.read_csv(path)
        same, diff = 0, []
        if category in ITEM_FMG:
            ko, en = merged(ko_item, ITEM_FMG[category]), merged(en_item, ITEM_FMG[category])
            for r in rows:
                gid = int(r["id"])
                official = ko.get(gid)
                if official is not None and official == r["ko"] and en.get(gid, "").replace("\u2019", "'") == r["en"].replace("\u2019", "'"):
                    same += 1
                    if args.apply:
                        r.update(source="game-text", status="ok", note=note)
                else:
                    diff.append((r["id"], r["en"], r["ko"], official))
        else:
            for r in rows:
                kind, en_name = r["id"].split(":", 1)
                key = TERM_EN_ALIASES.get(en_name, en_name).lower() if kind == "armorPart" else en_name.lower()
                candidates = terms_index.get(key, set())
                if r["ko"] in candidates:
                    same += 1
                    if args.apply:
                        r.update(source="game-text", status="ok", note=f"{note} (GR_MenuText)")
                else:
                    diff.append((r["id"], r["en"], r["ko"], sorted(candidates)[:3]))
        print(f"{category}: 일치 {same} / 다름·없음 {len(diff)}")
        for d in diff[:10]:
            print("   ", d)
        if diff:
            exit_code = 1
        if args.apply:
            with path.open("w", encoding="utf-8", newline="") as f:
                w = csv.writer(f, lineterminator="\n")
                w.writerow(cg.OUTPUT_COLUMNS)
                for r in rows:
                    w.writerow([r[c] for c in cg.OUTPUT_COLUMNS])
    if args.apply:
        print("반영했습니다. 이어서: python glossary/tools/check_glossary.py all && python glossary/tools/export_names.py")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
