#!/usr/bin/env python3
import polib

PO_PATH = '/Users/comfan/Documents/GitHub/AIERP/apps/erpnext/erpnext/locale/zh.po'
po = polib.pofile(PO_PATH)

for entry in po:
    if not entry.msgstr and entry.msgid:
        raw = entry.msgid
        if 'The Batch {0} of an item {1} has negative stock' in raw:
            entry.msgstr = raw.replace(
                'The Batch {0} of an item {1} has negative stock in the warehouse {2}{3}.',
                '物料 {1} 的批次 {0} 在仓库 {2}{3} 中存在负库存。'
            ).replace(
                'Please add a stock quantity of {4} to proceed with this entry.',
                '请添加 {4} 的库存数量以继续此分录。'
            ).replace(
                "If it is not possible to make an adjustment entry, please enable 'Allow Negative Stock for Batch' in Stock Settings to proceed.",
                '如果无法进行调整分录，请在库存设置中启用\u201c允许批次负库存\u201d以继续。'
            ).replace(
                'However, enabling this setting may lead to negative stock in the system.',
                '但是，启用此设置可能导致系统中出现负库存。'
            ).replace(
                'So please ensure the stock levels are adjusted as soon as possible to maintain the correct valuation rate.',
                '因此请尽快调整库存水平以保持正确的估值费率。'
            )
        elif 'Image in the description has been removed' in raw:
            entry.msgstr = '描述中的图片已被移除。要禁用此行为，请在 {1} 中取消勾选\u201c{0}\u201d。'
        elif 'Selling rate for item' in raw and 'is lower than its' in raw:
            entry.msgstr = '第 {0} 行：物料 {1} 的销售费率低于其 {2}。销售 {3} 应至少为 {4}。<br><br>或者，您可以在 {6} 中禁用\'{5}\'以绕过此验证。'
        elif 'Consumed Qty' in raw and 'must be less than or equal to Available Qty' in raw:
            entry.msgstr = '第 {0} 行：消耗数量 {1} {2} 必须小于或等于消耗物料表中的可用消耗数量 {3} {4}。'

po.save(PO_PATH)

po2 = polib.pofile(PO_PATH)
remaining = sum(1 for e in po2 if not e.msgstr and e.msgid)
print(f"ERPNext remaining untranslated: {remaining}")
