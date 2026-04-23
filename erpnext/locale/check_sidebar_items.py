#!/usr/bin/env python3
"""Check ALL workspace sidebar labels for missing translations."""
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

# Find all workspace sidebar JSON files (not doctype definition files)
sidebar_files = []
for base_dir in [
    '/Users/comfan/Documents/GitHub/AIERP/apps/erpnext/erpnext/workspace_sidebar',
    '/Users/comfan/Documents/GitHub/AIERP/apps/frappe/frappe/workspace_sidebar',
    '/Users/comfan/Documents/GitHub/AIERP/apps/hrms/hrms/workspace_sidebar',
]:
    if os.path.exists(base_dir):
        for f in os.listdir(base_dir):
            if f.endswith('.json'):
                sidebar_files.append(os.path.join(base_dir, f))

untranslated = []
all_labels = []

for filepath in sidebar_files:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        app = 'erpnext'
        if '/frappe/' in filepath:
            app = 'frappe'
        elif '/hrms/' in filepath:
            app = 'hrms'
        
        # Check title
        title = data.get('title', '')
        if title:
            translated = all_translations.get(title, '')
            all_labels.append({'label': title, 'translated': translated, 'type': 'Sidebar Title', 'app': app, 'file': os.path.basename(filepath)})
            if not translated:
                untranslated.append({'label': title, 'type': 'Sidebar Title', 'app': app, 'file': os.path.basename(filepath)})
        
        # Check items
        for item in data.get('items', []):
            item_label = item.get('label', '')
            if item_label:
                translated = all_translations.get(item_label, '')
                all_labels.append({'label': item_label, 'translated': translated, 'type': f"Item ({item.get('type', '')})", 'app': app, 'file': os.path.basename(filepath)})
                if not translated:
                    untranslated.append({'label': item_label, 'type': f"Item ({item.get('type', '')})", 'app': app, 'file': os.path.basename(filepath)})
    except Exception as e:
        print(f"Error: {filepath}: {e}")

print(f"Total sidebar labels: {len(all_labels)}")
print(f"Untranslated: {len(untranslated)}")
print()

# Show all untranslated
seen = set()
for i, item in enumerate(untranslated):
    key = item['label']
    if key not in seen:
        seen.add(key)
        print(f'{len(seen)}. "{key}" ({item["type"]}, {item["app"]}/{item["file"]})')

print()
print("=== All sidebar titles and their translations ===")
seen_titles = set()
for item in all_labels:
    if item['type'] == 'Sidebar Title' and item['label'] not in seen_titles:
        seen_titles.add(item['label'])
        status = "✅" if item['translated'] else "❌"
        print(f'{status} "{item["label"]}" → "{item["translated"]}" ({item["app"]})')
