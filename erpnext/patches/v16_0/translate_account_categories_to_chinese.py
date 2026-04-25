# Copyright (c) 2026, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe

from erpnext.accounts.doctype.financial_report_template.financial_report_engine import (
	FormulaFieldUpdater,
)


def execute():
	"""
	Patch to translate Account Category names from English to Chinese
	and update all Financial Report Template formulas accordingly
	"""
	# 1. Define English to Chinese mapping with descriptions
	category_data = {
		"现金及现金等价物": {
			"description": "库存现金、活期存款以及期限短、流动性强、易于转换为已知金额现金且价值变动风险很小的投资。例如：库存现金、银行活期存款、货币市场基金、期限≤3个月的国库券。",
		},
		"销售成本": {
			"description": "与销售商品直接相关的成本。例如：原材料、库存商品。",
		},
		"应交税费": {
			"description": "当期和以前期间的所得税义务。例如：所得税准备、预缴税款、代扣代缴税款。",
		},
		"财务费用": {
			"description": "利息和融资相关费用。例如：借款利息、银行手续费、租赁利息、汇兑损失。",
		},
		"无形资产": {
			"description": "可辨认的没有实物形态的非货币性资产。例如：软件、专利、商标、许可证、开发成本。",
		},
		"投资收益": {
			"description": "财务投资和现金管理产生的回报。例如：利息收入、股息收入、租金收入、公允价值收益。",
		},
		"长期借款": {
			"description": "期限超过一年的带息债务。例如：定期贷款、债券、信用债券、抵押贷款。",
		},
		"长期投资": {
			"description": "为战略目的或长期持有的投资。例如：股权投资、债券、联营企业、合营企业、存款。",
		},
		"长期预计负债": {
			"description": "期限超过一年的现时义务，时间或金额不确定。例如：资产弃置义务、环境治理、法律和解。",
		},
		"营业费用": {
			"description": "日常业务活动中发生的除直接成本外的费用。例如：销售费用、管理费用、营销费用、水电费、租金。",
		},
		"其他流动资产": {
			"description": "未归入其他类别的流动资产，包括预付费用和预付款项。例如：预付保险费、预付租金、供应商预付款、一年内可收回的保证金。",
		},
		"其他流动负债": {
			"description": "未归入其他类别的短期义务。例如：应计费用、法定负债、应付职工薪酬。",
		},
		"其他直接成本": {
			"description": "除销售成本外的直接成本。例如：直接人工、制造费用、进货运费。",
		},
		"其他非流动资产": {
			"description": "未归入其他类别的长期资产。例如：保证金、长期预付款、资本货物预付款。",
		},
		"其他非流动负债": {
			"description": "未归入其他类别的长期义务。例如：长期存款、递延收入、政府补助。",
		},
		"其他业务收入": {
			"description": "与业务活动相关的附带收入，非核心收入。例如：废料销售、政府补助、保险理赔、汇兑收益。",
		},
		"其他应付款": {
			"description": "非贸易应付款项，对供应商以外的各方的义务。例如：应付职工薪酬、应计费用、客户预付款、收到的保证金。",
		},
		"其他应收款": {
			"description": "非贸易应收款项，不包括融资安排。例如：员工预付款、保险理赔、退税、可收回的保证金。",
		},
		"盈余公积": {
			"description": "从利润或股本溢价中提取的累积利润和其他准备金。例如：一般准备金、留存收益、法定准备金、股本溢价。",
		},
		"营业收入": {
			"description": "日常活动中主要业务活动产生的收入。例如：商品销售收入、服务收入、佣金收入、特许权使用费收入。",
		},
		"股本": {
			"description": "已发行和已缴足股本股票的面值。例如：普通股、优先股。",
		},
		"短期借款": {
			"description": "一年内到期的带息债务。例如：银行透支、短期贷款、长期借款的流动部分。",
		},
		"短期投资": {
			"description": "为短期投资目的而持有、易于转换为现金的金融工具。例如：有价证券、期限>3个月的定期存款、共同基金。",
		},
		"短期预计负债": {
			"description": "一年内到期的现时义务，时间或金额不确定。例如：保修准备、法律索赔、重组费用。",
		},
		"存货资产": {
			"description": "库存和存货相关资产，包括原材料、在产品、产成品和库存商品。例如：原材料、产成品、贸易商品、消耗品。",
		},
		"有形资产": {
			"description": "用于业务活动的实物资产，包括不动产、厂房和设备。例如：土地、建筑物、机器设备、车辆、家具、在建工程。",
		},
		"税费支出": {
			"description": "当期和递延所得税义务。例如：当期所得税准备、递延所得税费用、预扣税。",
		},
		"应付账款": {
			"description": "欠供应商的款项。例如：供应商发票、应计采购、应付票据。",
		},
		"应收账款": {
			"description": "客户因购买商品或接受服务而在日常经营活动中欠付的款项。例如：应收账款、客户应收票据、未开票收入。",
		},
	}

	# 2. Update Account Category descriptions in database
	update_account_category_descriptions(category_data)

	# 3. Update Financial Report Template formulas
	update_financial_report_formulas()


def update_account_category_descriptions(data: dict[str, dict]):
	"""Update Account Category descriptions to Chinese"""
	for category_name, info in data.items():
		if frappe.db.exists("Account Category", category_name):
			try:
				frappe.db.set_value("Account Category", category_name, "description", info["description"])
				frappe.db.commit()
				print(f"已更新描述: {category_name}")
			except Exception as e:
				frappe.db.rollback()
				print(f"更新描述失败 {category_name}: {str(e)}")


def update_financial_report_formulas():
	"""Update all Financial Report Row formulas that reference account categories"""
	# Mapping from old English names to new Chinese names
	mapping = {
		"Cash and Cash Equivalents": "现金及现金等价物",
		"Cost of Goods Sold": "销售成本",
		"Current Tax Liabilities": "应交税费",
		"Finance Costs": "财务费用",
		"Intangible Assets": "无形资产",
		"Investment Income": "投资收益",
		"Long-term Borrowings": "长期借款",
		"Long-term Investments": "长期投资",
		"Long-term Provisions": "长期预计负债",
		"Operating Expenses": "营业费用",
		"Other Current Assets": "其他流动资产",
		"Other Current Liabilities": "其他流动负债",
		"Other Direct Costs": "其他直接成本",
		"Other Non-current Assets": "其他非流动资产",
		"Other Non-current Liabilities": "其他非流动负债",
		"Other Operating Income": "其他业务收入",
		"Other Payables": "其他应付款",
		"Other Receivables": "其他应收款",
		"Reserves and Surplus": "盈余公积",
		"Revenue from Operations": "营业收入",
		"Share Capital": "股本",
		"Short-term Borrowings": "短期借款",
		"Short-term Investments": "短期投资",
		"Short-term Provisions": "短期预计负债",
		"Stock Assets": "存货资产",
		"Tangible Assets": "有形资产",
		"Tax Expense": "税费支出",
		"Trade Payables": "应付账款",
		"Trade Receivables": "应收账款",
	}

	rows = frappe.get_all(
		"Financial Report Row",
		filters={
			"calculation_formula": ["like", "%account_category%"],
		},
		fields=["name", "calculation_formula"],
	)

	if not rows:
		return

	row_dict = {row.name: row.calculation_formula for row in rows}

	updater = FormulaFieldUpdater(
		field_name="account_category",
		value_mapping=mapping,
		exclude_operators=["like", "not like"],
	)

	updated_rows = updater.update_in_rows(row_dict)

	if updated_rows:
		print(f"已更新 {len(updated_rows)} 条财务报表行公式")
