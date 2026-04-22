#!/usr/bin/env python3
"""Export all untranslated entries from all zh.po files."""

import polib
import json

files = {
    'ERPNext': 'apps/erpnext/erpnext/locale/zh.po',
    'Frappe': 'apps/frappe/frappe/locale/zh.po',
    'HRMS': 'apps/hrms/hrms/locale/zh.po',
}

for name, path in files.items():
    po = polib.pofile(path)
    untranslated = []
    for entry in po:
        if not entry.msgstr and entry.msgid:
            untranslated.append({
                'msgid': entry.msgid,
                'comment': entry.comment or '',
                'occurrences': [f"{o[0]}:{o[1]}" for o in entry.occurrences],
            })
    
    print(f"=== {name}: {len(untranslated)} untranslated ===")
    for i, e in enumerate(untranslated):
        comment_str = f" ({e['comment'][:80]})" if e['comment'] else ""
        print(f'{i+1}. "{e["msgid"]}"{comment_str}')
    print()
