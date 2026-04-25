# Copyright (c) 2026, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe


def execute():
	"""
	Rollback patch - restore Accounting Dimension names from Chinese back to English
	"""
	dimension_mapping = {
		"分支机构": "Branch",
		"部门": "Department",
		"员工": "Employee",
		"地点": "Location",
	}

	for old_name, new_name in dimension_mapping.items():
		if frappe.db.exists("Accounting Dimension", old_name):
			try:
				frappe.rename_doc(
					"Accounting Dimension",
					old_name,
					new_name,
					force=True,
					merge=False,
				)
				frappe.db.commit()
				print(f"已恢复: {old_name} -> {new_name}")
			except Exception as e:
				frappe.db.rollback()
				print(f"恢复失败 {old_name}: {str(e)}")

	print("辅助核算名称已恢复为英文！")
