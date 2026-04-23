#!/usr/bin/env python3
"""Extract ALL Number Card and Dashboard Chart labels from all apps and check translation status."""

import json
import os
import polib

# Load all zh.po files from ALL apps
po_files = []
locale_dirs = []
for base_dir in ['/Users/comfan/Documents/GitHub/AIERP/apps']:
    for app in os.listdir(base_dir):
        locale_path = os.path.join(base_dir, app, app, 'locale', 'zh.po')
        if os.path.exists(locale_path):
            po_files.append((app, locale_path))

all_translations = {}
for app, path in po_files:
    po = polib.pofile(path)
    for entry in po:
        if entry.msgstr:
            all_translations[entry.msgid] = entry.msgstr

print(f"Total translations loaded: {len(all_translations)}")
print()

# Find all Number Card JSON files
number_card_labels = []
chart_labels = []

for base_dir in ['/Users/comfan/Documents/GitHub/AIERP/apps']:
    for app in os.listdir(base_dir):
        app_dir = os.path.join(base_dir, app, app)
        if not os.path.isdir(app_dir):
            continue
        
        # Number Cards
        nc_dir = os.path.join(app_dir, 'number_card')
        if os.path.isdir(nc_dir):
            for root, dirs, files in os.walk(nc_dir):
                for f in files:
                    if f.endswith('.json') and not f.startswith('__'):
                        filepath = os.path.join(root, f)
                        try:
                            with open(filepath, 'r', encoding='utf-8') as fh:
                                data = json.load(fh)
                            label = data.get('label', data.get('name', ''))
                            if label:
                                translated = all_translations.get(label, '')
                                number_card_labels.append({
                                    'label': label,
                                    'translated': translated,
                                    'app': app,
                                    'file': f,
                                })
                        except:
                            pass
        
        # Dashboard Charts
        dc_dir = os.path.join(app_dir, 'dashboard_chart')
        if os.path.isdir(dc_dir):
            for root, dirs, files in os.walk(dc_dir):
                for f in files:
                    if f.endswith('.json') and not f.startswith('__'):
                        filepath = os.path.join(root, f)
                        try:
                            with open(filepath, 'r', encoding='utf-8') as fh:
                                data = json.load(fh)
                            label = data.get('label', data.get('name', ''))
                            chart_type = data.get('type', '')
                            if label:
                                translated = all_translations.get(label, '')
                                chart_labels.append({
                                    'label': label,
                                    'translated': translated,
                                    'type': chart_type,
                                    'app': app,
                                    'file': f,
                                })
                        except:
                            pass

# Also check workspace JSON files for inline charts and number_cards
for base_dir in ['/Users/comfan/Documents/GitHub/AIERP/apps']:
    for app in os.listdir(base_dir):
        app_dir = os.path.join(base_dir, app, app)
        if not os.path.isdir(app_dir):
            continue
        
        for root, dirs, files in os.walk(app_dir):
            if '/workspace/' not in root:
                continue
            for f in files:
                if f.endswith('.json') and not f.startswith('__'):
                    filepath = os.path.join(root, f)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as fh:
                            data = json.load(fh)
                        
                        for ch in data.get('charts', []):
                            ch_label = ch.get('label', '')
                            if ch_label:
                                translated = all_translations.get(ch_label, '')
                                chart_labels.append({
                                    'label': ch_label,
                                    'translated': translated,
                                    'type': 'workspace_inline',
                                    'app': app,
                                    'file': f,
                                })
                        
                        for nc in data.get('number_cards', []):
                            nc_label = nc.get('label', '')
                            if nc_label:
                                translated = all_translations.get(nc_label, '')
                                number_card_labels.append({
                                    'label': nc_label,
                                    'translated': translated,
                                    'app': app,
                                    'file': f,
                                })
                    except:
                        pass

# Print results
print(f"=== Number Cards ({len(number_card_labels)}) ===")
nc_untranslated = [n for n in number_card_labels if not n['translated']]
nc_translated = [n for n in number_card_labels if n['translated']]
print(f"Translated: {len(nc_translated)}, Untranslated: {len(nc_untranslated)}")
print()

seen = set()
for item in nc_untranslated:
    if item['label'] not in seen:
        seen.add(item['label'])
        print(f'❌ "{item["label"]}" ({item["app"]}/{item["file"]})')

print()
print(f"=== Dashboard Charts ({len(chart_labels)}) ===")
ch_untranslated = [c for c in chart_labels if not c['translated']]
ch_translated = [c for c in chart_labels if c['translated']]
print(f"Translated: {len(ch_translated)}, Untranslated: {len(ch_untranslated)}")
print()

seen = set()
for item in ch_untranslated:
    if item['label'] not in seen:
        seen.add(item['label'])
        print(f'❌ "{item["label"]}" ({item["app"]}/{item["file"]})')

# Also show translated ones for reference
print()
print("=== Already Translated Number Cards ===")
seen = set()
for item in nc_translated:
    if item['label'] not in seen:
        seen.add(item['label'])
        print(f'✅ "{item["label"]}" → "{item["translated"]}"')

print()
print("=== Already Translated Charts ===")
seen = set()
for item in ch_translated:
    if item['label'] not in seen:
        seen.add(item['label'])
        print(f'✅ "{item["label"]}" → "{item["translated"]}"')
