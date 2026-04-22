#!/usr/bin/env python3
"""Update zh.po with remaining Chinese translations for accounts module entries."""

import polib

PO_PATH = '/Users/comfan/Documents/GitHub/AIERP/apps/erpnext/erpnext/locale/zh.po'

translations = {
    "<0":
        "<0",
    "A new fiscal year has been automatically created.":
        "新会计年度已自动创建。",
    "Accounting Onboarding":
        "会计入门引导",
    "Accounts Setup":
        "会计设置",
    "Add vouchers to generate preview.":
        "添加凭证以生成预览。",
    "Analytical Accounting":
        "分析性会计",
    "Apply discounts and margins on products":
        "对产品应用折扣和利润率",
    "Automatically Fetch Payment Terms from Order/Quotation":
        "自动从订单/报价单获取付款条件",
    "Base Tax Withheld":
        "本位币预扣税额",
    "Base Taxable Amount":
        "本位币应税金额",
    "COA Importer":
        "科目表导入器",
    "Cannot cancel this document as it is linked with the submitted Asset Value Adjustment <b>{0}</b>. Please cancel the Asset Value Adjustment to continue.":
        "无法取消此文档，因为它与已提交的资产价值调整 <b>{0}</b> 相关联。请先取消资产价值调整以继续。",
    "Cannot fetch selected rows for submitted Payment Request":
        "无法获取已提交付款请求的所选行",
    "Cannot merge {0} '{1}' into '{2}' as both have existing accounting entries in different currencies for company '{3}'.":
        "无法将 {0} '{1}' 合并到 '{2}'，因为两者在公司 '{3}' 中存在不同币种的会计分录。",
    "Cannot update rate as item {0} is already ordered or purchased against this quotation":
        "无法更新费率，因为物料 {0} 已针对此报价单订购或采购",
    "Check if this tax is not applicable to items (distinct from 0% rate)":
        "勾选表示此税率不适用于物料（与 0% 税率不同）",
}

po = polib.pofile(PO_PATH)

updated = 0

for entry in po:
    if not entry.msgstr and entry.msgid in translations:
        has_accounts = False
        for occ in entry.occurrences:
            if occ[0] and 'accounts' in occ[0]:
                has_accounts = True
                break
        
        if has_accounts:
            entry.msgstr = translations[entry.msgid]
            updated += 1

print(f"Updated {updated} entries")

po.save(PO_PATH)
print(f"Saved to {PO_PATH}")

po2 = polib.pofile(PO_PATH)
remaining_accounts = 0
for entry in po2:
    if not entry.msgstr and entry.msgid:
        for occ in entry.occurrences:
            if occ[0] and 'accounts' in occ[0]:
                remaining_accounts += 1
                break

print(f"Remaining untranslated entries from accounts module: {remaining_accounts}")
