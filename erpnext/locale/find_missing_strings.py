#!/usr/bin/env python3
"""Extract ALL translatable strings from accounts module source code and find ones missing from zh.po."""

import polib
import os
import re
import json

ACCOUNTS_DIR = '/Users/comfan/Documents/GitHub/AIERP/apps/erpnext/erpnext/accounts'
PO_PATH = '/Users/comfan/Documents/GitHub/AIERP/apps/erpnext/erpnext/locale/zh.po'

def extract_python_strings(directory):
    strings = set()
    # Match _("...") and _('...')
    pattern1 = re.compile(r'_\(\s*"((?:[^"\\]|\\.)*)"\s*\)')
    pattern2 = re.compile(r"_\(\s*'((?:[^'\\]|\\.)*)'\s*\)")
    
    for root, dirs, files in os.walk(directory):
        for f in files:
            if f.endswith('.py'):
                filepath = os.path.join(root, f)
                try:
                    with open(filepath, 'r', encoding='utf-8') as fh:
                        content = fh.read()
                        for m in pattern1.findall(content):
                            if m.strip():
                                strings.add(m)
                        for m in pattern2.findall(content):
                            if m.strip():
                                strings.add(m)
                except:
                    pass
    return strings

def extract_js_strings(directory):
    strings = set()
    pattern1 = re.compile(r'__\(\s*"((?:[^"\\]|\\.)*)"\s*[\),]')
    pattern2 = re.compile(r"__\(\s*'((?:[^'\\]|\\.)*)'\s*[\),]")
    
    for root, dirs, files in os.walk(directory):
        for f in files:
            if f.endswith('.js'):
                filepath = os.path.join(root, f)
                try:
                    with open(filepath, 'r', encoding='utf-8') as fh:
                        content = fh.read()
                        for m in pattern1.findall(content):
                            if m.strip():
                                strings.add(m)
                        for m in pattern2.findall(content):
                            if m.strip():
                                strings.add(m)
                except:
                    pass
    return strings

def extract_json_strings(directory):
    strings = set()
    for root, dirs, files in os.walk(directory):
        for f in files:
            if f.endswith('.json') and f not in ['__init__.json', 'boilerplate.json', 'country_info.json']:
                filepath = os.path.join(root, f)
                try:
                    with open(filepath, 'r', encoding='utf-8') as fh:
                        content = fh.read()
                        data = json.loads(content)
                        # Extract from common translatable fields
                        for key in ['label', 'description', 'title', 'message', 'subject', 'data']:
                            if key in data and isinstance(data[key], str) and data[key].strip():
                                text = data[key].strip()
                                # Only include strings with English letters
                                if any(c.isalpha() and ord(c) < 128 for c in text):
                                    strings.add(text)
                        # Extract from fields array
                        if 'fields' in data and isinstance(data['fields'], list):
                            for field in data['fields']:
                                if isinstance(field, dict):
                                    for key in ['label', 'description']:
                                        if key in field and isinstance(field[key], str) and field[key].strip():
                                            text = field[key].strip()
                                            if any(c.isalpha() and ord(c) < 128 for c in text):
                                                strings.add(text)
                        # Extract from options (Select field options)
                        if 'fields' in data and isinstance(data['fields'], list):
                            for field in data['fields']:
                                if isinstance(field, dict) and field.get('fieldtype') == 'Select' and 'options' in field:
                                    opts = field['options']
                                    if isinstance(opts, str):
                                        for opt in opts.split('\n'):
                                            opt = opt.strip()
                                            if opt and any(c.isalpha() and ord(c) < 128 for c in opt):
                                                strings.add(opt)
                except:
                    pass
    return strings

# Also check HTML templates
def extract_html_strings(directory):
    strings = set()
    pattern = re.compile(r'_\(\s*"((?:[^"\\]|\\.)*)"\s*\)')
    
    for root, dirs, files in os.walk(directory):
        for f in files:
            if f.endswith('.html'):
                filepath = os.path.join(root, f)
                try:
                    with open(filepath, 'r', encoding='utf-8') as fh:
                        content = fh.read()
                        for m in pattern.findall(content):
                            if m.strip():
                                strings.add(m)
                except:
                    pass
    return strings

# Load zh.po
po = polib.pofile(PO_PATH)
po_msgids = set(entry.msgid for entry in po)

# Extract strings from accounts module
py_strings = extract_python_strings(ACCOUNTS_DIR)
js_strings = extract_js_strings(ACCOUNTS_DIR)
json_strings = extract_json_strings(ACCOUNTS_DIR)
html_strings = extract_html_strings(ACCOUNTS_DIR)

all_strings = py_strings | js_strings | json_strings | html_strings

# Find strings NOT in zh.po
missing = all_strings - po_msgids

# Filter out non-translatable strings
skip_patterns = [
    r'^[a-z_]+$',  # single lowercase words (likely variable names)
    r'^\d+$',  # just numbers
    r'^_{1,2}$',  # just underscores
    r'^\s*$',  # whitespace only
    r'^[A-Z]{1,3}$',  # very short abbreviations like CC, Dr
    r'^_Test',  # test strings
    r'^\{',  # starts with {
    r'^<',  # HTML tags
]

def should_skip(s):
    for pattern in skip_patterns:
        if re.match(pattern, s):
            return True
    # Skip very short strings (likely abbreviations or codes)
    if len(s) <= 2:
        return True
    # Skip strings that are just field names
    if re.match(r'^[a-z][a-z_]*$', s):
        return True
    return False

missing_filtered = sorted([s for s in missing if not should_skip(s)])

print(f"Python _() strings: {len(py_strings)}")
print(f"JavaScript __() strings: {len(js_strings)}")
print(f"JSON strings: {len(json_strings)}")
print(f"HTML strings: {len(html_strings)}")
print(f"Total unique strings from accounts module: {len(all_strings)}")
print(f"Already in zh.po: {len(all_strings & po_msgids)}")
print(f"Missing from zh.po (filtered): {len(missing_filtered)}")
print()

for i, s in enumerate(missing_filtered):
    print(f'{i+1}. "{s}"')
