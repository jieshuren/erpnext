#!/usr/bin/env python3
"""Final verification of all zh.po files."""
import polib

files = {
    'ERPNext': '/Users/comfan/Documents/GitHub/AIERP/apps/erpnext/erpnext/locale/zh.po',
    'Frappe': '/Users/comfan/Documents/GitHub/AIERP/apps/frappe/frappe/locale/zh.po',
    'HRMS': '/Users/comfan/Documents/GitHub/AIERP/apps/hrms/hrms/locale/zh.po',
}

total_all = 0
translated_all = 0
untranslated_all = 0

for name, path in files.items():
    po = polib.pofile(path)
    total = len(po)
    translated = sum(1 for e in po if e.msgstr and e.msgid)
    untranslated = sum(1 for e in po if not e.msgstr and e.msgid)
    total_all += total
    translated_all += translated
    untranslated_all += untranslated
    print(f"=== {name} ===")
    print(f"Total: {total}, Translated: {translated}, Untranslated: {untranslated}, Coverage: {translated/total*100:.1f}%")

print()
print(f"=== TOTAL ===")
print(f"Total: {total_all}, Translated: {translated_all}, Untranslated: {untranslated_all}, Coverage: {translated_all/total_all*100:.1f}%")
