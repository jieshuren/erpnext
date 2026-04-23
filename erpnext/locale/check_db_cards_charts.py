#!/usr/bin/env python3
"""Check translation status of Number Card and Dashboard Chart names from database."""

import polib

# Load all zh.po files
po_files = [
    '/Users/comfan/Documents/GitHub/AIERP/apps/erpnext/erpnext/locale/zh.po',
    '/Users/comfan/Documents/GitHub/AIERP/apps/frappe/frappe/locale/zh.po',
    '/Users/comfan/Documents/GitHub/AIERP/apps/hrms/hrms/locale/zh.po',
    '/Users/comfan/Documents/GitHub/AIERP/apps/eps/eps/locale/zh.po',
    '/Users/comfan/Documents/GitHub/AIERP/apps/blog/blog/locale/zh.po',
    '/Users/comfan/Documents/GitHub/AIERP/apps/newsletter/newsletter/locale/zh.po',
]

all_translations = {}
for path in po_files:
    po = polib.pofile(path)
    for entry in po:
        if entry.msgstr:
            all_translations[entry.msgid] = entry.msgstr

# Dashboard Chart names from database
charts = [
    "Accounts Payable Ageing", "Accounts Receivable Ageing", "Appraisal Overview",
    "Asset Value Analytics", "Attendance Count", "Background Job Activity",
    "Bank Balance", "Budget Variance", "Category-wise Asset Value",
    "Claims by Type", "Completed Operation", "Completed Projects",
    "Delivery Trends", "Department Wise Employee Count",
    "Department wise Expense Claims", "Department Wise Openings",
    "Department Wise Salary(Last Month)", "Department wise Timesheet Hours",
    "Designation Wise Employee Count", "Designation Wise Openings",
    "Designation Wise Salary(Last Month)", "Email Activity",
    "Employee Advance Status", "Employees by Age", "Employees by Branch",
    "Employees by Grade", "Employees by Type", "Expense Claims",
    "Gender Diversity Ratio", "Grievance Type", "Hiring vs Attrition Count",
    "Incoming Bills (Purchase Invoice)", "Incoming Leads",
    "Interview Status", "Item Shortage Summary",
    "Item-wise Annual Sales", "Job Applicant Pipeline",
    "Job Applicant Source", "Job Applicants by Country",
    "Job Application Frequency", "Job Application Status",
    "Job Card Analysis", "Job Offer Status",
    "Last Month Downtime Analysis", "Lead Source",
    "Location-wise Asset Value", "Login", "Login Activity",
    "Material Request Analysis", "Notifications By Type",
    "Oldest Items", "Opportunities via Campaigns",
    "Opportunity Trends", "Outgoing Bills (Sales Invoice)",
    "Outgoing Salary", "Pending Work Order", "Produced Quantity",
    "Profit and Loss", "Project Summary",
    "Purchase Order Analysis", "Purchase Order Trends",
    "Purchase Receipt Trends", "Quality Inspection Analysis",
    "Quality Inspections", "Sales Order Analysis",
    "Sales Order Trends", "Shift Assignment Breakup",
    "Stock Value by Item Group", "Subcontracting Order",
    "Territory Wise Opportunity Count", "Territory Wise Sales",
    "Timesheet Activity Breakup", "Top Customers", "Top Suppliers",
    "Training Type", "Warehouse wise Stock Value",
    "Webpage Views", "Won Opportunities",
    "Work Order Analysis", "Work Order Qty Analysis",
    "Y-O-Y Promotions", "Y-O-Y Transfers",
]

# Number Card names from database
number_cards = [
    "Active Employees", "Annual Salary", "Average Expense Claim",
    "Average Hours Worked", "Employees on Leave Today",
    "Expense Claims", "Holidays in this Month",
    "Incoming Bills", "Leaves Pending Approval",
    "New Hires (Last Month)", "Outgoing Bills",
    "Total Employees", "Unpaid Expense Claims",
]

print("=== Dashboard Charts ===")
ch_missing = []
for name in charts:
    translated = all_translations.get(name, '')
    if translated:
        print(f'✅ "{name}" → "{translated}"')
    else:
        print(f'❌ "{name}"')
        ch_missing.append(name)

print()
print("=== Number Cards ===")
nc_missing = []
for name in number_cards:
    translated = all_translations.get(name, '')
    if translated:
        print(f'✅ "{name}" → "{translated}"')
    else:
        print(f'❌ "{name}"')
        nc_missing.append(name)

print()
print(f"Charts: {len(charts) - len(ch_missing)}/{len(charts)} translated, {len(ch_missing)} missing")
print(f"Number Cards: {len(number_cards) - len(nc_missing)}/{len(number_cards)} translated, {len(nc_missing)} missing")
