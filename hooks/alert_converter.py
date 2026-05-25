"""
MkDocs hook: converts GitHub-style alerts to MkDocs Material admonitions.

GitHub format:
    > [!NOTE]
    > Content line

MkDocs format:
    !!! note
        Content line
"""
import re

ALERT_MAP = {
    'NOTE': 'note',
    'TIP': 'tip',
    'IMPORTANT': 'important',
    'WARNING': 'warning',
    'CAUTION': 'danger',
}


def on_page_markdown(markdown, **kwargs):
    def _convert(m):
        kind = ALERT_MAP.get(m.group(1).upper(), 'note')
        body = re.sub(r'^>[ \t]?', '', m.group(2), flags=re.MULTILINE).rstrip()
        indented = '\n'.join(f'    {line}' for line in body.splitlines())
        return f'!!! {kind}\n{indented}\n\n'

    return re.sub(
        r'> \[!([A-Z]+)\]\n((?:>[ \t][^\n]*\n?|>[^\n]*\n?)+)',
        _convert,
        markdown,
    )
