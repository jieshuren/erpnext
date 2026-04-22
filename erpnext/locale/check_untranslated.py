#!/usr/bin/env python3
"""Find all untranslated entries in zh.po that belong to the accounts module."""

import polib

PO_PATH = '/Users/comfan/Documents/GitHub/AIERP/apps/erpnext/erpnext/locale/zh.po'

po = polib.pofile(PO_PATH)

# Find all untranslated entries with accounts module occurrences
accounts_untranslated = []
all_untranslated = []

for entry in po:
    if not entry.msgstr and entry.msgid:
        all_untranslated.append(entry)
        # Check if any occurrence is in the accounts module
        has_accounts = False
        for occ in entry.occurrences:
            if occ[0] and 'accounts' in occ[0]:
                has_accounts = True
                break
        if has_accounts:
            accounts_untranslated.append(entry)

print(f"Total entries in zh.po: {len(po)}")
print(f"Total untranslated entries: {len(all_untranslated)}")
print(f"Untranslated entries from accounts module: {len(accounts_untranslated)}")
print()

for i, entry in enumerate(accounts_untranslated):
    occ_str = ', '.join([f"{o[0]}:{o[1]}" for o in entry.occurrences if 'accounts' in o[0]])
    comment_str = f" ({entry.comment})" if entry.comment else ""
    print(f'{i+1}. "{entry.msgid}"{comment_str}')
    print(f'   @ {occ_str}')
    print()
