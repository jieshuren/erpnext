# Copyright (c) 2026, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe


def execute():
	"""
	Patch to keep only common countries and translate them to Chinese
	"""
	# 常用国家映射（英文原名 -> 中文名称）
	common_countries = {
		"China": "中国",
		"United States": "美国",
		"Japan": "日本",
		"Germany": "德国",
		"United Kingdom": "英国",
		"France": "法国",
		"South Korea": "韩国",
		"Singapore": "新加坡",
		"Malaysia": "马来西亚",
		"Thailand": "泰国",
		"Vietnam": "越南",
		"India": "印度",
		"Indonesia": "印度尼西亚",
		"Philippines": "菲律宾",
		"Australia": "澳大利亚",
		"Canada": "加拿大",
		"Brazil": "巴西",
		"Russia": "俄罗斯",
		"Italy": "意大利",
		"Spain": "西班牙",
		"Mexico": "墨西哥",
		"United Arab Emirates": "阿联酋",
	}
	
	# 1. 先翻译常用国家名称
	for old_name, new_name in common_countries.items():
		if frappe.db.exists("Country", old_name):
			try:
				frappe.rename_doc(
					"Country",
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
	
	# 2. 删除其他不常用的国家
	all_countries = frappe.get_all("Country", pluck="name")
	keep_countries = set(common_countries.values())
	
	to_delete = [c for c in all_countries if c not in keep_countries]
	
	# 检查是否被引用
	referenced_doctypes = [
		"Address",
		"Customer",
		"Supplier",
		"Company",
		"Lead",
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
	
	# 删除不常用的国家
	for country in safe_to_delete:
		try:
			frappe.delete_doc("Country", country, force=True)
			frappe.db.commit()
			print(f"已删除: {country}")
		except Exception as e:
			frappe.db.rollback()
			print(f"删除失败 {country}: {str(e)}")
	
	print(f"\n完成！保留了 {len(keep_countries)} 个常用国家")
	print(f"删除了 {len(safe_to_delete)} 个不常用的国家")
