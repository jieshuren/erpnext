# Copyright (c) 2026, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe


def execute():
	"""
	Patch to remove unused English mode of payments, keeping only Chinese ones
	"""
	# 保留的中文付款方式
	keep_payments = {"现金", "昆仑银行"}
	
	# 获取所有付款方式
	all_mops = frappe.get_all("Mode of Payment", pluck="name")
	
	# 找出要删除的英文付款方式
	to_delete = [m for m in all_mops if m not in keep_payments]
	
	if not to_delete:
		print("没有需要删除的付款方式")
		return
	
	# 检查是否被引用
	referenced_doctypes = [
		"Payment Entry",
		"Sales Invoice",
		"Purchase Invoice",
		"Journal Entry",
		"POS Invoice",
	]
	
	safe_to_delete = []
	
	for mop in to_delete:
		is_referenced = False
		for doctype in referenced_doctypes:
			if frappe.db.exists(doctype, {"mode_of_payment": mop}):
				print(f"跳过 {mop}: 被 {doctype} 引用")
				is_referenced = True
				break
		
		if not is_referenced:
			safe_to_delete.append(mop)
	
	# 删除未使用的英文付款方式
	for mop in safe_to_delete:
		try:
			frappe.delete_doc("Mode of Payment", mop, force=True)
			frappe.db.commit()
			print(f"已删除: {mop}")
		except Exception as e:
			frappe.db.rollback()
			print(f"删除失败 {mop}: {str(e)}")
	
	print(f"\n完成！保留了 {', '.join(keep_payments)}")
	print(f"删除了 {len(safe_to_delete)} 个未使用的付款方式")
