#!/usr/bin/env python3
"""Update zh.po with Chinese translations for ALL untranslated accounts module entries."""

import polib

PO_PATH = '/Users/comfan/Documents/GitHub/AIERP/apps/erpnext/erpnext/locale/zh.po'

translations = {
    "Cannot cancel Stock Reservation Entry {0}, as it has used in the work order {1}. Please cancel the work order first or unreserved the stock":
        "无法取消库存预留分录 {0}，因为它已在工单 {1} 中使用。请先取消工单或取消库存预留",
    "Cannot delete an item which has been ordered":
        "无法删除已订购的物料",
    "Cannot reduce quantity than ordered or purchased quantity":
        "无法减少到低于已订购或已采购的数量",
    "Check row {0} for account {1}: Party Type is only allowed for Receivable or Payable accounts":
        "请检查第 {0} 行科目 {1}：往来单位类型仅允许用于应收或应付科目",
    "Check row {0} for account {1}: Party is only allowed if Party Type is set":
        "请检查第 {0} 行科目 {1}：仅在设置了往来单位类型时才允许填写往来单位",
    "Clearance date changed from {0} to {1} via Bank Clearance Tool":
        "通过银行对账工具将清算日期从 {0} 更改为 {1}",
    "Company Account is mandatory":
        "公司账户为必填项",
    "Company Address is missing. You don't have permission to create an Address. Please contact your System Manager.":
        "公司地址缺失。您没有创建地址的权限。请联系系统管理员。",
    "Configure Chart of Accounts":
        "配置科目表",
    "Consider for Tax Withholding":
        "考虑预扣税",
    "Consider for Tax Withholding ":
        "考虑预扣税",
    "Created By Migration":
        "由迁移创建",
    "Cumulative Threshold":
        "累计阈值",
    "Custom Remark":
        "自定义备注",
    "Deduct Tax On Basis":
        "扣税依据",
    "Deducted From":
        "扣减自",
    "Default Ageing Range":
        "默认账龄范围",
    "Direct return is not allowed for Timesheet.":
        "不允许直接退回工时表。",
    "Disable Cumulative Threshold":
        "禁用累计阈值",
    "Disable Transaction Threshold":
        "禁用交易阈值",
    "Don't Recompute Tax":
        "不重新计算税额",
    "Duplicate Payment Schedule selected":
        "选择了重复的付款计划",
    "Edit Tax Withholding Entries":
        "编辑预扣税分录",
    "Enable Accounting Dimensions":
        "启用会计维度",
    "Enable Discounts and Margin":
        "启用折扣和利润率",
    "Enable Loyalty Point Program":
        "启用积分计划",
    "Enable Subscription":
        "启用订阅",
    "Enable Subscription tracking in invoice":
        "在发票中启用订阅跟踪",
    "Enable cost center, projects and other custom accounting dimensions":
        "启用成本中心、项目和其他自定义会计维度",
    "Exclude Zero Balance Parties":
        "排除零余额往来单位",
    "FX Revaluation":
        "汇率重估",
    "Fetch Payment Schedule In Payment Request":
        "在付款请求中获取付款计划",
    "Fiscal Year Details":
        "会计年度详情",
    "From Date and To Date are required":
        "起始日期和结束日期为必填项",
    "Grand Total (Company Currency":
        "合计（公司本位币",
    "Grand Total (Transaction Currency)":
        "合计（交易币种）",
    "Grand Total must match sum of Payment References":
        "合计金额必须与付款参考之和匹配",
    "Gross Total":
        "毛总额",
    "Group Name":
        "组名称",
    "If party does not exist, create it using the Customer Name field.":
        "如果客户不存在，请使用客户名称字段创建。",
    "If party does not exist, create it using the Supplier Name field.":
        "如果供应商不存在，请使用供应商名称字段创建。",
    "Ignore Tax Withholding Threshold":
        "忽略预扣税阈值",
    "Incoming Bills":
        "进项账单",
    "Incoming Payment":
        "收款",
    "Invalid Accounting Dimension":
        "无效的会计维度",
    "Learn about <a href=\"https://docs.frappe.io/erpnext/user/manual/en/common_party_accounting\" rel=\"noopener noreferrer\">Common Party</a>":
        "了解<a href=\"https://docs.frappe.io/erpnext/user/manual/en/common_party_accounting\" rel=\"noopener noreferrer\">共用往来单位</a>",
    "New Fiscal Year - {0}":
        "新会计年度 - {0}",
    "No Tax withholding account set for Company {0} in Tax Withholding Category {1}.":
        "公司 {0} 在预扣税类别 {1} 中未设置预扣税科目。",
    "Opening Invoice Tool":
        "期初发票工具",
    "Others":
        "其他",
    "Outgoing Bills":
        "销项账单",
    "Outgoing Payment":
        "付款",
    "Party ID":
        "往来单位编号",
    "Payment Options":
        "付款选项",
    "Payment Requests made from Sales / Purchase Invoice will be put in Draft explicitly":
        "从销售/采购发票创建的付款请求将明确设为草稿状态",
    "Payment Schedule based Payment Requests cannot be created because a Payment Entry already exists for this document.":
        "无法创建基于付款计划的付款请求，因为此单据已存在付款分录。",
    "Payment methods refreshed. Please review before proceeding.":
        "付款方式已刷新。请在继续之前进行审核。",
    "Please review the {0} configuration and complete any required financial setup activities.":
        "请审核 {0} 配置并完成任何必要的财务设置活动。",
    "Repost":
        "重新过账",
    "Review Accounts Settings":
        "审核会计设置",
    "Review Chart of Accounts":
        "审核科目表",
    "Row #{0}: Cannot create entry with different taxable AND withholding document links.":
        "第 {0} 行：无法创建应税和预扣单据链接不同的分录。",
    "Row #{0}: Cannot delete item {1} which is already ordered against this Sales Order.":
        "第 {0} 行：无法删除物料 {1}，该物料已针对此销售订单订购。",
    "Row #{0}: Could not find enough {1} entries to match. Remaining amount: {2}":
        "第 {0} 行：找不到足够的 {1} 分录进行匹配。剩余金额：{2}",
    "Row #{0}: Dates overlapping with other row in group {1}":
        "第 {0} 行：日期与组 {1} 中的其他行重叠",
    "Row #{0}: Withholding Amount {1} does not match calculated amount {2}.":
        "第 {0} 行：预扣金额 {1} 与计算金额 {2} 不匹配。",
    "Row #{0}:Quantity for Item {1} cannot be zero.":
        "第 {0} 行：物料 {1} 的数量不能为零。",
    "Row #{}: Either Party ID or Party Name is required":
        "第 {} 行：往来单位编号或名称为必填项",
    "Row #{}: Party ID is required":
        "第 {} 行：往来单位编号为必填项",
    "Row {0}: Sales Invoice {1} is already created for {2}":
        "第 {0} 行：已为 {2} 创建销售发票 {1}",
    "Sales Taxes":
        "销售税",
    "Sell quantity cannot exceed the asset quantity. Asset {0} has only {1} item(s).":
        "销售数量不能超过资产数量。资产 {0} 仅有 {1} 个项目。",
    "Stock Update Not Allowed":
        "不允许更新库存",
    "Stock cannot be updated for Purchase Invoice {0} because a Purchase Receipt {1} has already been created for this transaction. Please disable the 'Update Stock' checkbox in the Purchase Invoice and save the invoice.":
        "无法更新采购发票 {0} 的库存，因为已为此交易创建了采购收货单 {1}。请在采购发票中取消勾选\u201c更新库存\u201d复选框并保存发票。",
    "Tax Rate %":
        "税率 %",
    "Tax Withholding Entries":
        "预扣税分录",
    "Tax Withholding Entry":
        "预扣税分录",
    "Tax Withholding Group":
        "预扣税组",
    "Tax withheld only for amount exceeding cumulative threshold":
        "仅对超过累计阈值的金额预扣税款",
    "The fiscal year has been automatically created in a Disabled state to maintain consistency with the previous fiscal year's status.":
        "会计年度已自动创建为禁用状态，以保持与上一会计年度状态的一致性。",
    "The following payment schedule(s) already exist:\n{0}":
        "以下付款计划已存在：\n{0}",
    "The outstanding amount {0} in {1} is lesser than {2}. Updating the outstanding to this invoice.":
        "{1} 中的未清金额 {0} 小于 {2}。正在将未清金额更新到此发票。",
    "Threshold Exemption":
        "阈值豁免",
    "Timesheet {0} cannot be invoiced in its current state":
        "工时表 {0} 在当前状态下无法开票",
    "Total Taxable Amount":
        "应税总额",
    "Totals (Company Currency)":
        "合计（公司本位币）",
    "Transaction Threshold":
        "交易阈值",
    "Transaction for which tax is withheld":
        "被预扣税款的交易",
    "Transaction from which tax is withheld":
        "从中预扣税款的交易",
    "UTM Analytics":
        "UTM 分析",
    "Under Withheld Reason":
        "少扣税原因",
    "View Balance Sheet":
        "查看资产负债表",
    "We can see {0} is made against {1}. If you want {1}'s outstanding to be updated, uncheck the '{2}' checkbox.":
        "我们可以看到 {0} 是针对 {1} 创建的。如果您希望更新 {1} 的未清金额，请取消勾选\u201c{2}\u201d复选框。",
    "When checked, only cumulative threshold will be applied":
        "勾选后，仅应用累计阈值",
    "When checked, only transaction threshold will be applied for transaction individually":
        "勾选后，仅对单笔交易应用交易阈值",
    "Withholding Document":
        "预扣单据",
    "You can use {0} to reconcile against {1} later.":
        "您可以稍后使用 {0} 与 {1} 进行对账。",
    "You don't have permission to create a Company Address. Please contact your System Manager.":
        "您没有创建公司地址的权限。请联系系统管理员。",
    "You don't have permission to update Company details. Please contact your System Manager.":
        "您没有更新公司详情的权限。请联系系统管理员。",
    "You don't have permission to update this document. Please contact your System Manager.":
        "您没有更新此文档的权限。请联系系统管理员。",
    "{0} is not a valid Accounting Dimension.":
        "{0} 不是有效的会计维度。",
    "{0} {1} not allowed to be reposted. You can enable it by adding it '{2}' table in {3}.":
        "{0} {1} 不允许重新过账。您可以通过在 {3} 的'{2}'表中添加来启用。",
    "{0}: {1} does not exist":
        "{0}：{1} 不存在",
}

po = polib.pofile(PO_PATH)

updated = 0

for entry in po:
    if not entry.msgstr and entry.msgid in translations:
        # Check if this entry has accounts module occurrences
        has_accounts = False
        for occ in entry.occurrences:
            if occ[0] and 'accounts' in occ[0]:
                has_accounts = True
                break
        
        if has_accounts:
            entry.msgstr = translations[entry.msgid]
            updated += 1

print(f"Updated {updated} entries")

# Save the file
po.save(PO_PATH)
print(f"Saved to {PO_PATH}")

# Verify - count remaining untranslated accounts entries
po2 = polib.pofile(PO_PATH)
remaining_accounts = 0
for entry in po2:
    if not entry.msgstr and entry.msgid:
        for occ in entry.occurrences:
            if occ[0] and 'accounts' in occ[0]:
                remaining_accounts += 1
                break

print(f"Remaining untranslated entries from accounts module: {remaining_accounts}")
