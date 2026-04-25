# Copyright (c) 2026, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe


def execute():
	"""
	Patch to remove unused currencies, keeping only CNY, USD, EUR
	"""
	keep_currencies = {"CNY", "USD", "EUR"}
	
	# Get all currencies
	all_currencies = frappe.get_all("Currency", pluck="name")
	
	# Enable USD and EUR if they exist
	for curr in ["USD", "EUR"]:
		if frappe.db.exists("Currency", curr):
			frappe.db.set_value("Currency", curr, "enabled", 1)
			print(f"已启用: {curr}")
	
	# Find currencies to delete
	to_delete = [c for c in all_currencies if c not in keep_currencies]
	
	if not to_delete:
		print("没有需要删除的币种")
		return
	
	# Check if any currency is referenced in transactions
	referenced_tables = [
		("Payment Entry", "paid_from"),
		("Payment Entry", "paid_to"),
		("Sales Invoice", "currency"),
		("Purchase Invoice", "currency"),
		("Journal Entry", "currency"),
		("GL Entry", "account_currency"),
	]
	
	safe_to_delete = []
	
	for curr in to_delete:
		is_referenced = False
		for doctype, field in referenced_tables:
			if frappe.db.exists(doctype, {"currency": curr}):
				print(f"跳过 {curr}: 被 {doctype} 引用")
				is_referenced = True
				break
		
		if not is_referenced:
			safe_to_delete.append(curr)
	
	# Delete safe currencies
	for curr in safe_to_delete:
		try:
			frappe.delete_doc("Currency", curr, force=True)
			frappe.db.commit()
			print(f"已删除: {curr}")
		except Exception as e:
			frappe.db.rollback()
			print(f"删除失败 {curr}: {str(e)}")
	
	print(f"\n完成！保留了 {', '.join(keep_currencies)}")
	print(f"删除了 {len(safe_to_delete)} 个未使用的币种")
