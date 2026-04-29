import pandas as pd
import frappe
import os

def strict_sync_202603():
    frappe.connect()
    excel_path = "/Users/comfan/Documents/GitHub/AIERP/财务数据/HuaShuo_凭证列表_202602-202603.xlsx"
    company_full = '大庆市华烁油气开采技术服务有限公司'
    
    print(f"Strict Syncing 2026-03 using ONLY entries from {excel_path}...")
    
    df = pd.read_excel(excel_path)
    df = df[df['凭证日期'].astype(str).str.contains('2026-03')]
    
    depts = {d.name.split(" - ")[0]: d.name for d in frappe.get_all("Department")}
    projects = {p.project_name: p.name for p in frappe.get_all("Project", fields=["name", "project_name"])}

    # 先清理，确保重新对齐
    print("Clearing 2026-03 dimensions for a fresh start...")
    frappe.db.sql(f"UPDATE `tabGL Entry` SET department=NULL, project=NULL WHERE posting_date LIKE '2026-03%%' AND company='{company_full}'")
    frappe.db.sql(f"UPDATE `tabJournal Entry Account` jea JOIN `tabJournal Entry` je ON jea.parent=je.name SET jea.department=NULL, jea.project=NULL WHERE je.posting_date LIKE '2026-03%%' AND je.company='{company_full}'")

    updated_rows = 0
    
    for _, row in df.iterrows():
        try:
            # 构造凭证匹配键
            v_type = str(row['凭证类别']).strip()
            v_no = str(int(row['凭证号'])).zfill(3)
            v_date = str(row['凭证日期'])[:10]
            match_key = f"{v_type}-{v_no}-{v_date}"
            
            # 获取 Excel 里的维度（如果为空则跳过更新）
            dept_name = str(row.get('部门')).strip() if pd.notnull(row.get('部门')) else None
            proj_name = str(row.get('项目')).strip() if pd.notnull(row.get('项目')) else None
            
            if not dept_name and not proj_name:
                continue
                
            target_dept = depts.get(dept_name)
            target_proj = projects.get(proj_name)
            
            # 找到 ERPNext 凭证
            je_name = frappe.db.get_value("Journal Entry", {"user_remark": match_key}, "name")
            if not je_name: continue
            
            acc_code = str(row['科目编码']).strip()
            debit = float(row['借方金额']) if pd.notnull(row['借方金额']) else 0
            credit = float(row['贷方金额']) if pd.notnull(row['贷方金额']) else 0
            
            # 寻找精准匹配的子表行 (锁定 parent, account, debit, credit)
            je_accs = frappe.get_all("Journal Entry Account", 
                filters={
                    "parent": je_name, 
                    "account": ["like", f"{acc_code}%"], 
                    "debit": debit, 
                    "credit": credit,
                    "department": ("is", "not set") # 优先填充还没填的
                }, 
                fields=["name", "account"],
                limit=1
            )
            
            if je_accs:
                ja = je_accs[0]
                # 更新子表
                frappe.db.set_value("Journal Entry Account", ja.name, {
                    "department": target_dept,
                    "project": target_proj
                }, update_modified=False)
                
                # 同步到总账 (GL Entry)
                # 注意：GL Entry 中可能没有 voucher_detail_no，必须通过金额和科目回追
                frappe.db.sql("""
                    UPDATE `tabGL Entry` 
                    SET department=%s, project=%s
                    WHERE voucher_no=%s AND account=%s AND ABS(debit-%s)<0.01 AND ABS(credit-%s)<0.01
                    AND (department IS NULL OR department = '')
                    LIMIT 1
                """, (target_dept, target_proj, je_name, ja.account, debit, credit))
                
                updated_rows += 1
                
        except:
            continue

    frappe.db.commit()
    print(f"Strict Sync Done! Updated {updated_rows} rows based on Excel detailed lines.")

if __name__ == "__main__":
    strict_sync_202603()
