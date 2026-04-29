import pandas as pd
import frappe
import os

def final_deep_reconcile():
    frappe.connect()
    path = "/Users/comfan/Documents/GitHub/AIERP/财务数据/HuaShuo_辅助余额表_部门_202501_202603 2026-04-29 11_12_26.xlsx"
    company_full = '大庆市华烁油气开采技术服务有限公司'
    
    print(f"Deep Reconciling (Cumulative 2025-01 to 2026-03)...")
    
    # 1. 提取 Excel 标准答案 (辅助余额表 - 借方发生额)
    df = pd.read_excel(path, skiprows=4, header=None)
    excel_map = {} # (dept, acc_name) -> amount
    for _, row in df.iterrows():
        dept = str(row[1]).strip()
        acc_name = str(row[2]).strip()
        try:
            amt = float(row[5]) if pd.notnull(row[5]) else 0
        except:
            continue
        if amt == 0 or '小计' in dept or '合计' in dept or dept == 'nan':
            continue
        key = (dept, acc_name)
        excel_map[key] = excel_map.get(key, 0) + amt

    # 2. 获取系统当前加总 (借方金额，因为辅助余额表统计的是借方发生)
    system_gl = frappe.db.sql(f"""
        SELECT 
            IFNULL(REPLACE(department, ' - 华烁', ''), '未分配部门') as dept,
            account,
            SUM(debit) as debit_amt
        FROM `tabGL Entry`
        WHERE posting_date >= '2025-01-01' AND posting_date <= '2026-03-31'
        AND company = '{company_full}'
        AND (account REGEXP '^[456]')
        AND voucher_type != 'Period Closing Voucher'
        AND is_opening = 'No'
        GROUP BY department, account
    """, as_dict=True)

    system_map = {}
    for r in system_gl:
        acc_parts = r['account'].split(' - ')
        acc_name = acc_parts[1] if len(acc_parts) > 1 else acc_parts[0]
        key = (r['dept'], acc_name)
        system_map[key] = system_map.get(key, 0) + float(r['debit_amt'])

    # 3. 打印存在差异的部门和科目
    print(f"\n{'部门':<15} | {'科目':<20} | {'Excel标准':>12} | {'系统现状':>12} | {'差异':>12}")
    print("-" * 85)
    
    all_keys = sorted(set(excel_map.keys()) | set(system_map.keys()))
    for key in all_keys:
        ex_val = excel_map.get(key, 0)
        sy_val = system_map.get(key, 0)
        diff = ex_val - sy_val
        
        if abs(diff) > 10: # 只看 10 元以上的显著差异
            print(f"{key[0]:<15} | {key[1]:<20} | {ex_val:>12,.2f} | {sy_val:>12,.2f} | {diff:>12,.2f}")

if __name__ == "__main__":
    final_deep_reconcile()
