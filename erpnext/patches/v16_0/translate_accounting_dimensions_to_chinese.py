# Copyright (c) 2026, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe


def execute():
	"""
	Patch to translate Accounting Dimension names from English to Chinese
	"""
	dimension_mapping = {
		"Branch": "分支机构",
		"Department": "部门",
		"Employee": "员工",
		"Location": "地点",
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
				print(f"已重命名: {old_name} -> {new_name}")
			except Exception as e:
				frappe.db.rollback()
				print(f"重命名失败 {old_name}: {str(e)}")

	# Also update label field for each dimension
	for old_name, new_name in dimension_mapping.items():
		if frappe.db.exists("Accounting Dimension", new_name):
			frappe.db.set_value("Accounting Dimension", new_name, "label", new_name)
			frappe.db.commit()

	print("辅助核算汉化完成！")
