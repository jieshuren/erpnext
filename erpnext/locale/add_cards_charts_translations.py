#!/usr/bin/env python3
"""Add translations for Dashboard Charts and Number Cards to ERPNext zh.po."""

import polib

PO_PATH = '/Users/comfan/Documents/GitHub/AIERP/apps/erpnext/erpnext/locale/zh.po'
po = polib.pofile(PO_PATH)

existing_msgids = set(entry.msgid for entry in po)

translations = {
    # Dashboard Charts - missing
    "Accounts Payable Ageing": "应付账款账龄",
    "Accounts Receivable Ageing": "应收账款账龄",
    "Background Job Activity": "后台任务活动",
    "Claims by Type": "按类型分的报销",
    "Delivery Trends": "交货趋势",
    "Department Wise Employee Count": "按部门分的员工数",
    "Department wise Expense Claims": "按部门分的费用报销",
    "Department Wise Salary(Last Month)": "按部门分的薪资（上月）",
    "Department wise Timesheet Hours": "按部门分的工时表小时数",
    "Designation Wise Employee Count": "按职位分的员工数",
    "Designation Wise Openings": "按职位分的空缺",
    "Designation Wise Salary(Last Month)": "按职位分的薪资（上月）",
    "Email Activity": "邮件活动",
    "Employee Advance Status": "员工预支状态",
    "Employees by Age": "按年龄分的员工",
    "Employees by Branch": "按分部分的员工",
    "Employees by Grade": "按等级分的员工",
    "Employees by Type": "按类型分的员工",
    "Gender Diversity Ratio": "性别多样性比例",
    "Hiring vs Attrition Count": "入职与离职人数",
    "Incoming Bills (Purchase Invoice)": "进项账单（采购发票）",
    "Incoming Leads": "新增线索",
    "Item Shortage Summary": "物料短缺汇总",
    "Item-wise Annual Sales": "按物料分的年销售额",
    "Job Applicant Pipeline": "职位申请人漏斗",
    "Job Applicants by Country": "按国家分的职位申请人",
    "Job Application Frequency": "职位申请频率",
    "Job Application Status": "职位申请状态",
    "Job Offer Status": "录用通知状态",
    "Location-wise Asset Value": "按位置分的资产价值",
    "Material Request Analysis": "物料需求分析",
    "Notifications By Type": "按类型分的通知",
    "Oldest Items": "最旧物料",
    "Opportunities via Campaigns": "通过营销活动获得的商机",
    "Opportunity Trends": "商机趋势",
    "Outgoing Bills (Sales Invoice)": "销项账单（销售发票）",
    "Shift Assignment Breakup": "班次分配分布",
    "Territory Wise Opportunity Count": "按区域分的商机数",
    "Territory Wise Sales": "按区域分的销售额",
    "Timesheet Activity Breakup": "工时表活动分布",
    "Top Customers": "顶级客户",
    "Top Suppliers": "顶级供应商",
    "Training Type": "培训类型",
    "Warehouse wise Stock Value": "按仓库分的库存价值",
    "Webpage Views": "网页浏览量",
    "Y-O-Y Promotions": "同比晋升",
    "Y-O-Y Transfers": "同比调动",
    # Number Cards - missing
    "Active Employees": "在职员工",
    "Average Expense Claim": "平均费用报销",
    "Average Hours Worked": "平均工作时长",
    "Employees on Leave Today": "今日请假员工",
    "Holidays in this Month": "本月节假日",
    "New Hires (Last Month)": "新入职员工（上月）",
    "Total Employees": "员工总数",
    "Unpaid Expense Claims": "未付款费用报销",
}

# Update existing entries or add new ones
updated = 0
added = 0

for msgid, msgstr in translations.items():
    found = False
    for entry in po:
        if entry.msgid == msgid:
            if not entry.msgstr:
                entry.msgstr = msgstr
                updated += 1
            found = True
            break
    
    if not found and msgid not in existing_msgids:
        entry = polib.POEntry(msgid=msgid, msgstr=msgstr)
        po.append(entry)
        added += 1

print(f"Updated {updated} existing entries")
print(f"Added {added} new entries")

po.save(PO_PATH)
print(f"Saved to {PO_PATH}")

# Verify
po2 = polib.pofile(PO_PATH)
remaining = sum(1 for e in po2 if not e.msgstr and e.msgid)
print(f"Total remaining untranslated in ERPNext zh.po: {remaining}")
