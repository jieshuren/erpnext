import pandas as pd
import frappe
import os

def full_period_reconcile():
    frappe.connect()
    excel_dir = "/Users/comfan/Documents/GitHub/AIERP/财务数据"
    target_file = None
    for f in os.listdir(excel_dir):
        if "辅助余额表_部门_202501_202603" in f and f.endswith(".xlsx"):
            target_file = os.path.join(excel_dir, f)
            break
            
    if not target_file:
        print("Target Excel file not found.")
        return

    print(f"Reading {target_file}...")
    company_full = '大庆市华烁油气开采技术服务有限公司'
    
    # 1. 解析 Excel (累计发生)
    # 根据预览，Row 4 以后是数据，索引 1 部门，索引 2 科目，索引 5 本期借方
    df = pd.read_excel(target_file, skiprows=4, header=None)
    excel_map = {} # key: (dept, account_name)
    for _, row in df.iterrows():
        dept = str(row[1]).strip()
        acc_name = str(row[2]).strip()
        try:
            amt = float(row[5]) if pd.notnull(row[5]) else 0
        except:
            continue
            
        if amt == 0 or dept == 'nan' or '小计' in dept or '合计' in dept:
            continue
            
        key = (dept, acc_name)
        excel_map[key] = excel_map.get(key, 0) + amt

    # 2. 获取系统总账明细 (2025-01 至 2026-03)
    system_gl = frappe.db.sql(f"""
        SELECT 
            REPLACE(department, ' - 华烁', '') as dept,
            account,
            SUM(debit - credit) as net_amt,
            SUM(debit) as debit_amt
        FROM `tabGL Entry`
        WHERE posting_date >= '2025-01-01' AND posting_date <= '2026-03-31'
        AND company = '{company_full}'
        AND (account REGEXP '^[456]')
        AND voucher_type != 'Period Closing Voucher'
        AND is_opening = 'No'
        GROUP BY department, account
    """, as_dict=True)

    system_map_net = {}
    system_map_debit = {}
    for r in system_gl:
        dept = r['dept'] or '未分配部门'
        acc_parts = r['account'].split(' - ')
        acc_name = acc_parts[1] if len(acc_parts) > 1 else acc_parts[0]
        
        key = (dept, acc_name)
        system_map_net[key] = system_map_net.get(key, 0) + float(r['net_amt'])
        system_map_debit[key] = system_map_debit.get(key, 0) + float(r['debit_amt'])

    # 3. 输出汇总对比 (按部门)
    print(f"\n{'部门':<15} | {'Excel借方':>15} | {'系统借方':>15} | {'系统净额':>15} | {'差异(对借方)':>15}")
    print("-" * 85)
    
    all_depts = sorted(set([k[0] for k in excel_map.keys()]) | set([k[0] for k in system_map_net.keys()]))
    
    total_ex = 0
    total_sy_debit = 0
    total_sy_net = 0

    for d in all_depts:
        ex_val = sum([v for k, v in excel_map.items() if k[0] == d])
        sy_debit = sum([v for k, v in system_map_debit.items() if k[0] == d])
        sy_net = sum([v for k, v in system_map_net.items() if k[0] == d])
        
        total_ex += ex_val
        total_sy_debit += sy_debit
        total_sy_net += sy_net

        if abs(ex_val) > 1 or abs(sy_debit) > 1:
            print(f"{d:<15} | {ex_val:>15,.2f} | {sy_debit:>15,.2f} | {sy_net:>15,.2f} | {ex_val - sy_debit:>15,.2f}")

    print("-" * 85)
    print(f"{'总计':<15} | {total_ex:>15,.2f} | {total_sy_debit:>15,.2f} | {total_sy_net:>15,.2f} | {total_ex - total_sy_debit:>15,.2f}")

if __name__ == "__main__":
    full_period_reconcile()
