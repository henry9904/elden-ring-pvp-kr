# 💾 New Save From Scratch

> [!NOTE]
> A step-by-step guide to creating a new PvP-ready character using Cheat Engine and the ER Inventory Planner.
> Original document by **Anti Mage Association** *(Content & Design: Momo & Poisson, 2025)*.
> Markdown redesign by **Crong**.

---

## 📋 Overview

| Step | What You Do | Where |
|------|-------------|-------|
| 1 | Create your build on the planner | Browser |
| 2 | Generate a Cheat Engine script | Browser |
| 3 | Copy the script (Cmd+A / Cmd+C) | Browser |
| 4 | Launch the game with DEN / DEN2 | Game |
| 5 | Create your character | Game |
| 6 | Apply checkboxes in Cheat Engine | Cheat Engine |
| 7 | Paste the inventory script | Cheat Engine |
| 8 | Apply Event Flags | Cheat Engine |
| 9 | Add runes and level up | Game + CE |
| 10 | Talk to Melina → Roundtable Hold | Game |

---

## 🖥️ Step 1 — Create Your Build

Go to the **[ER Inventory Planner](https://er-inventory.nyasu.business/)** and build your character.

> [!TIP]
> For a detailed walkthrough of the planner, refer to the video guide linked on the site.

Fill in your stats, weapons, talismans, and equipment. When done, navigate to the **Load/Save** tab and select **Cheat Engine**.

---

## 📋 Step 2 — Generate the Script

In the **Cheat Engine** tab of the planner:

1. Click **"Generate Script"** (bottom right of the page)
2. The script is now ready to be copied

> [!NOTE]
> This script spawns all weapons and talismans in order in-game to avoid manually sorting your inventory.
> - Use this **while offline only**
> - Open the table, copy the output, and place it as a script under `MassItemGib` → `ItemGib` — then enable it
> - **Spawns weapons at your current max upgrade level** — make sure you have upgraded at least one weapon to your target level first
> - Requires: `Scripts → Build Creation → ItemGib` enabled
> - See the video guide on acquisition order to match in-game sort order

---

## 📋 Step 3 — Copy the Script

Press **`Cmd+A`** then **`Cmd+C`** (or `Ctrl+A` / `Ctrl+C` on Windows) to copy the entire script output from the browser.

---

## 🎮 Step 4 — Launch the Game

Launch the game using the **mod launch file** — either **DEN** or **DEN2**.

> [!IMPORTANT]
> You must use the DEN mod launcher, not the standard game launcher.

Create your character according to your build (class, body type, appearance).

---

## ⚙️ Step 5 — Cheat Engine: Enable Required Checkboxes

The following steps take place inside **Cheat Engine** with *The Grand Archives* table loaded.

Enable the following checkboxes under `Scripts → Build Creation`:

### ✅ Required Checkboxes

```
[X] Scripts
    [X] Build Creation
        [ ] AddSoul
        [X] ItemGib
            [ ] Item
            [ ] Quantity
            [ ] Upgrade
            [ ] Reinforcement Level (Regular | Somber)
            [ ] Ash of War
            [ ] > Spawn Item
            [ ] Details
        [X] MassItemGib
            [ ] Give build starting items
            [X] Give all prattling pates       ← Paste your script here
            [ ] -- Base Game --
            [ ] Give all weapons
            ...
```

> [!IMPORTANT]
> Inside **`Give all prattling pates`**, you need to select the script entry.
> Then go to the **Edit menu**, select all the existing code (`Cmd+A` / `Ctrl+A` + Delete), and paste the code you copied from the builder. Click **OK**.

---

## ⚙️ Step 6 — Enable Additional Checkboxes

In the following section, simply **select the marked checkboxes**:

```
MassItemGib
    [ ] Give all accessories
    [ ] Give all ashes of war
    -- Goods --
        [ ] Give misc consumables
        [ ] Give all crafting materials
        [ ] Give all upgrade materials
        [ ] Give all limited quantity craftables
        [ ] Give all greases
        [X] Give all spirit ashes          ← Select this
        [ ] Give all sorceries
        [ ] Give all incantations
        [ ] Give all crystal tears
        [ ] Give all bell bearings
    -- Shadow of the Erdtree --
        [ ] Give all weapons (SotE)
        ...
        [X] Give all crystal tears (SotE)  ← Select this
        [ ] Give all bell bearings (SotE)

[ ] Warp
[ ] Set flask level
[X] Add charge to flask                    ← Select this
[ ] Unlock All Gestures
[ ] Upgrades Need No Materials
```

> [!CAUTION]
> **Don't forget to add charge to flasks!** — Select `Add charge to flask` and enter **12** when prompted (value between 0 and 12).

---

## ⚙️ Step 7 — Enable Event Flags

Next, go to **Event Flags** and select the checkboxes one by one:

```
[X] Event Flags
    [ ] Unlock all...
        [X] Unlock all Graces              ← Select
        [X] Unlock all Whetblades          ← Select
        [X] Unlock all Cookbooks           ← Select
        [X] Unlock all Maps                ← Select
        [X] Unlock all Summoning Pools     ← Select
        [X] Unlock all Colosseums          ← Select
    [ ] Invasion Regions
    [ ] Save Character Flags
    [ ] Event Flags by ID
    [ ] Deprecated
```

> [!WARNING]
> **Your game may crash unexpectedly during this process — this is normal.**
> Simply relaunch the game (reopen it within the mod launcher) and continue from where you left off.

---

## ⚙️ Step 8 — Add Runes to Level Up

Back in Cheat Engine, under `Scripts → Build Creation → AddSoul`:

1. Double-click **Runes** and change the value to `999999999`
2. Select the **`> Give Runes`** checkbox to apply them

> [!TIP]
> You will see your rune count update in-game. This gives you enough runes to reach your target level.

---

## 🎮 Step 9 — Return to the Game

Go back into the game.

1. Move to the **nearest Grace**
2. Talk to **Melina** to gain the ability to level up
3. Level your character to match your build's stats
4. Talk to Melina again — accept the offer to travel to the **Roundtable Hold**

> [!NOTE]
> Visiting the Roundtable Hold is required to **activate the arena** for PvP.

---

## ⚠️ Important — Morgott's Rune (Fight Club)

> [!IMPORTANT]
> To participate in the **fight club**, you must activate **Morgott's Rune**.
>
> After adding it through Cheat Engine, you need to **activate it at a Grace** in-game.

---

## ✅ Done!

You are ready to play. Welcome to the DEN.

---

*Special thanks to our developers 👥👑*

| Name | Role |
|------|------|
| **Emiia** | Elden Ring Planner |
| **Axi** | DEN2 Creator |

---

<div align="center">

*Content and design by Momo & Poisson · Anti Mage Association, 2025*
*Markdown redesign by Crong*

</div>
