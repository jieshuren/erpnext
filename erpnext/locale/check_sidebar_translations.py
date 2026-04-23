#!/usr/bin/env python3
"""Check if workspace labels have translations in zh.po files."""
import polib
import json

# Workspace labels from database
workspace_labels = [
    "Assets", "Blog", "Build", "Buying", "CRM", "EPS", "ERPNext Settings",
    "Expenses", "Financial Reports", "Home", "HR Setup", "Integrations",
    "Invoicing", "Leaves", "Manufacturing", "Payroll", "Performance",
    "Projects", "Quality", "Recruitment", "Selling", "Shift & Attendance",
    "Stock", "Subcontracting", "Support", "Tax & Benefits", "Tenure",
    "Users", "Website", "Welcome Workspace",
]

# Also get workspace sidebar items
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

print("=== Workspace Labels Translation Status ===")
for label in workspace_labels:
    translated = all_translations.get(label, '')
    status = "✅" if translated else "❌"
    print(f'{status} "{label}" → "{translated}"')

# Also check common sidebar link labels that might be missing
print()
print("=== Checking common DocType names used as sidebar links ===")
# These are common DocType names that appear as sidebar links
doctype_names = [
    "Company", "Customer", "Supplier", "Item", "Account",
    "Cost Center", "Warehouse", "Sales Order", "Purchase Order",
    "Sales Invoice", "Purchase Invoice", "Payment Entry",
    "Journal Entry", "Delivery Note", "Purchase Receipt",
    "Quotation", "Material Request", "Stock Entry",
    "Fiscal Year", "Budget", "Project", "Task",
    "Employee", "Salary Structure", "Salary Slip",
    "Leave Application", "Leave Type", "Leave Allocation",
    "Attendance", "Shift Type", "Expense Claim",
    "Asset", "Asset Category", "Asset Depreciation Schedule",
    "Bank Account", "Bank Transaction", "Payment Reconciliation",
    "POS Profile", "POS Invoice", "Dunning",
    "Loyalty Program", "Promotional Scheme",
    "Tax Withholding Category", "Tax Rule",
    "Exchange Rate Revaluation",
    "General Ledger", "Trial Balance", "Balance Sheet",
    "Profit and Loss Statement", "Cash Flow",
    "Accounts Receivable", "Accounts Payable",
    "Chart of Accounts", "Opening Invoice Tool",
]

for name in doctype_names:
    translated = all_translations.get(name, '')
    status = "✅" if translated else "❌"
    if not translated:
        print(f'{status} "{name}"')
