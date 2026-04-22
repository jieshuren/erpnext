#!/usr/bin/env python3
"""Export all untranslated msgids from each zh.po to a text file for translation."""

import polib

files = {
    'erpnext': 'apps/erpnext/erpnext/locale/zh.po',
    'frappe': 'apps/frappe/frappe/locale/zh.po',
    'hrms': 'apps/hrms/hrms/locale/zh.po',
}

for app_name, path in files.items():
    po = polib.pofile(path)
    untranslated = []
    for entry in po:
        if not entry.msgstr and entry.msgid:
            untranslated.append(entry.msgid)
    
    out_path = f'/Users/comfan/Documents/GitHub/AIERP/apps/erpnext/erpnext/locale/untranslated_{app_name}.txt'
    with open(out_path, 'w', encoding='utf-8') as f:
        for msgid in untranslated:
            # Use a delimiter that won't appear in the msgid
            f.write(msgid.replace('\n', '\\n') + '\n')
    
    print(f"{app_name}: {len(untranslated)} untranslated entries exported to {out_path}")
