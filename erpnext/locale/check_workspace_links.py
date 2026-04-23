#!/usr/bin/env python3
"""Extract ALL labels from workspace JSON files and check which ones lack translations."""
import json
import os
import polib

# Load all zh.po
po_files = {
    'erpnext': polib.pofile('/Users/comfan/Documents/GitHub/AIERP/apps/erpnext/erpnext/locale/zh.po'),
    'frappe': polib.pofile('/Users/comfan/Documents/GitHub/AIERP/apps/frappe/frappe/locale/zh.po'),
    'hrms': polib.pofile('/Users/comfan/Documents/GitHub/AIERP/apps/hrms/hrms/locale/zh.po'),
}

all_translations = {}
for app, po in po_files.items():
    for entry in po:
        if entry.msgstr:
            all_translations[entry.msgid] = entry.msgstr

# Find all workspace JSON files
workspace_files = []
for base_dir in [
    '/Users/comfan/Documents/GitHub/AIERP/apps/erpnext/erpnext',
    '/Users/comfan/Documents/GitHub/AIERP/apps/frappe/frappe',
    '/Users/comfan/Documents/GitHub/AIERP/apps/hrms/hrms',
]:
    for root, dirs, files in os.walk(base_dir):
        for f in files:
            if f.endswith('.json') and '/workspace/' in root:
                workspace_files.append(os.path.join(root, f))

untranslated_labels = set()
all_labels = set()

for filepath in workspace_files:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Check all labels
        for key in ['label', 'title']:
            val = data.get(key, '')
            if val:
                all_labels.add(val)
                if not all_translations.get(val, ''):
                    untranslated_labels.add(val)
        
        # Check links
        for link in data.get('links', []):
            for key in ['label', 'description']:
                val = link.get(key, '')
                if val:
                    all_labels.add(val)
                    if not all_translations.get(val, ''):
                        untranslated_labels.add(val)
        
        # Check shortcuts
        for sc in data.get('shortcuts', []):
            val = sc.get('label', '')
            if val:
                all_labels.add(val)
                if not all_translations.get(val, ''):
                    untranslated_labels.add(val)
        
        # Check charts
        for ch in data.get('charts', []):
            val = ch.get('label', '')
            if val:
                all_labels.add(val)
                if not all_translations.get(val, ''):
                    untranslated_labels.add(val)
                    
    except Exception as e:
        pass

print(f"Total unique labels in workspace JSONs: {len(all_labels)}")
print(f"Untranslated labels: {len(untranslated_labels)}")
print()
for i, label in enumerate(sorted(untranslated_labels)):
    print(f'{i+1}. "{label}"')
