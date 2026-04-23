#!/usr/bin/env python3
"""Extract ALL workspace labels and link labels from workspace JSON files and check translation status."""

import json
import os
import polib

# All workspace JSON files
workspace_files = []

for base_dir in [
    '/Users/comfan/Documents/GitHub/AIERP/apps/erpnext/erpnext',
    '/Users/comfan/Documents/GitHub/AIERP/apps/frappe/frappe',
    '/Users/comfan/Documents/GitHub/AIERP/apps/hrms/hrms',
]:
    for root, dirs, files in os.walk(base_dir):
        for f in files:
            if f.endswith('.json') and '/workspace/' in root and root.endswith(f.split('.')[0]):
                workspace_files.append(os.path.join(root, f))

# Load all zh.po files
po_files = {
    'erpnext': polib.pofile('/Users/comfan/Documents/GitHub/AIERP/apps/erpnext/erpnext/locale/zh.po'),
    'frappe': polib.pofile('/Users/comfan/Documents/GitHub/AIERP/apps/frappe/frappe/locale/zh.po'),
    'hrms': polib.pofile('/Users/comfan/Documents/GitHub/AIERP/apps/hrms/hrms/locale/zh.po'),
}

# Build translation lookup
all_translations = {}
for app, po in po_files.items():
    for entry in po:
        if entry.msgstr:
            all_translations[entry.msgid] = entry.msgstr

# Extract labels from workspace JSONs
all_labels = set()
workspace_labels = []

for filepath in workspace_files:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        app = 'erpnext'
        if '/frappe/' in filepath:
            app = 'frappe'
        elif '/hrms/' in filepath:
            app = 'hrms'
        
        # Workspace label and title
        label = data.get('label', '')
        title = data.get('title', '')
        
        if label:
            all_labels.add(label)
            translated = all_translations.get(label, '')
            workspace_labels.append({
                'type': 'Workspace Label',
                'label': label,
                'translated': translated,
                'file': os.path.basename(filepath),
                'app': app,
            })
        
        if title and title != label:
            all_labels.add(title)
            translated = all_translations.get(title, '')
            workspace_labels.append({
                'type': 'Workspace Title',
                'label': title,
                'translated': translated,
                'file': os.path.basename(filepath),
                'app': app,
            })
        
        # Links
        for link in data.get('links', []):
            link_label = link.get('label', '')
            if link_label:
                all_labels.add(link_label)
                translated = all_translations.get(link_label, '')
                workspace_labels.append({
                    'type': f"Link ({link.get('type', 'unknown')})",
                    'label': link_label,
                    'translated': translated,
                    'file': os.path.basename(filepath),
                    'app': app,
                })
        
        # Shortcuts
        for sc in data.get('shortcuts', []):
            sc_label = sc.get('label', '')
            if sc_label:
                all_labels.add(sc_label)
                translated = all_translations.get(sc_label, '')
                workspace_labels.append({
                    'type': 'Shortcut',
                    'label': sc_label,
                    'translated': translated,
                    'file': os.path.basename(filepath),
                    'app': app,
                })
        
        # Charts
        for ch in data.get('charts', []):
            ch_label = ch.get('label', '')
            if ch_label:
                all_labels.add(ch_label)
                translated = all_translations.get(ch_label, '')
                workspace_labels.append({
                    'type': 'Chart',
                    'label': ch_label,
                    'translated': translated,
                    'file': os.path.basename(filepath),
                    'app': app,
                })
        
        # Number cards
        for nc in data.get('number_cards', []):
            nc_label = nc.get('label', '')
            if nc_label:
                all_labels.add(nc_label)
                translated = all_translations.get(nc_label, '')
                workspace_labels.append({
                    'type': 'Number Card',
                    'label': nc_label,
                    'translated': translated,
                    'file': os.path.basename(filepath),
                    'app': app,
                })
        
        # Quick lists
        for ql in data.get('quick_lists', []):
            ql_label = ql.get('label', '')
            if ql_label:
                all_labels.add(ql_label)
                translated = all_translations.get(ql_label, '')
                workspace_labels.append({
                    'type': 'Quick List',
                    'label': ql_label,
                    'translated': translated,
                    'file': os.path.basename(filepath),
                    'app': app,
                })
                
    except Exception as e:
        print(f"Error reading {filepath}: {e}")

# Find untranslated labels
untranslated = [w for w in workspace_labels if not w['translated']]

print(f"Total workspace labels found: {len(workspace_labels)}")
print(f"Untranslated: {len(untranslated)}")
print()

# Group by type
from collections import defaultdict
by_type = defaultdict(list)
for w in untranslated:
    by_type[w['type']].append(w)

for type_name, items in by_type.items():
    print(f"=== {type_name} ({len(items)} untranslated) ===")
    seen = set()
    for item in items:
        if item['label'] not in seen:
            seen.add(item['label'])
            print(f'  "{item["label"]}" ({item["app"]}/{item["file"]})')
    print()
