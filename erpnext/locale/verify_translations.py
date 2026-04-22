#!/usr/bin/env python3
"""Final verification of zh.po translation status for accounts module."""

import polib

PO_PATH = '/Users/comfan/Documents/GitHub/AIERP/apps/erpnext/erpnext/locale/zh.po'
po = polib.pofile(PO_PATH)

total = len(po)
translated = sum(1 for e in po if e.msgstr and e.msgid)
untranslated = sum(1 for e in po if not e.msgstr and e.msgid)

accounts_total = 0
accounts_translated = 0
accounts_untranslated = 0
accounts_untranslated_list = []

for entry in po:
    for occ in entry.occurrences:
        if occ[0] and 'accounts' in occ[0]:
            accounts_total += 1
            if entry.msgstr:
                accounts_translated += 1
            else:
                accounts_untranslated += 1
                accounts_untranslated_list.append(entry.msgid)
            break

print("=== zh.po Overall ===")
print(f"Total: {total}")
print(f"Translated: {translated}")
print(f"Untranslated: {untranslated}")
print(f"Coverage: {translated/total*100:.1f}%")
print()
print("=== Accounts Module ===")
print(f"Total: {accounts_total}")
print(f"Translated: {accounts_translated}")
print(f"Untranslated: {accounts_untranslated}")
if accounts_total > 0:
    print(f"Coverage: {accounts_translated/accounts_total*100:.1f}%")

if accounts_untranslated_list:
    print()
    print("Untranslated entries:")
    for i, msgid in enumerate(accounts_untranslated_list):
        print(f'  {i+1}. "{msgid}"')
