# Copyright (c) 2026, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe


def execute():
	"""
	Patch to remove unused countries, keeping only China
	"""
	keep_country = "China"
	
	# Get all countries
	all_countries = frappe.get_all("Country", pluck="name")
	
	# Find countries to delete
	to_delete = [c for c in all_countries if c != keep_country]
	
	if not to_delete:
		print("没有需要删除的国家")
		return
	
	# Check if any country is referenced in transactions
	referenced_doctypes = [
		"Address",
		"Customer",
		"Supplier",
		"Company",
		"Lead",
		"Sales Invoice",
		"Purchase Invoice",
		"Delivery Note",
		"Purchase Order",
	]
	
	safe_to_delete = []
	
	for country in to_delete:
		is_referenced = False
		for doctype in referenced_doctypes:
			if frappe.db.exists(doctype, {"country": country}):
				print(f"跳过 {country}: 被 {doctype} 引用")
				is_referenced = True
				break
		
		if not is_referenced:
			safe_to_delete.append(country)
	
	# Delete safe countries
	for country in safe_to_delete:
		try:
			frappe.delete_doc("Country", country, force=True)
			frappe.db.commit()
			print(f"已删除: {country}")
		except Exception as e:
			frappe.db.rollback()
			print(f"删除失败 {country}: {str(e)}")
	
	print(f"\n完成！保留了 {keep_country}")
	print(f"删除了 {len(safe_to_delete)} 个未使用的国家")
