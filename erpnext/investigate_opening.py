import frappe

def run():
    print("--- 今日期初分录统计 ---")
    res = frappe.db.sql("""
        SELECT 
            voucher_no, 
            voucher_type,
            SUM(debit) as total_debit, 
            COUNT(*) as entries_count,
            MIN(creation) as first_entry,
            MAX(creation) as last_entry
        FROM `tabGL Entry` 
        WHERE is_opening = 'Yes' 
        AND creation > '2026-04-28' 
        GROUP BY voucher_no
    """, as_dict=True)
    
    if not res:
        print("今日未发现新增的标记为 'is_opening' 的 GL Entry。")
    else:
        for r in res:
            print(f"凭证: {r.voucher_no} ({r.voucher_type}), 总借方: {r.total_debit}, 分录数: {r.entries_count}, 创建时间: {r.first_entry}")

    print("\n--- 期间结转凭证 (Period Closing Voucher) ---")
    try:
        pcv = frappe.get_all("Period Closing Voucher", 
            filters={"creation": [">", "2026-04-28"]}, 
            fields=["name", "creation", "owner"])
        
        if not pcv:
            print("今日未发现新增的期间结转凭证。")
        else:
            for p in pcv:
                print(f"结转凭证: {p.name}, 创建人: {p.owner}, 创建时间: {p.creation}")
    except Exception as e:
        print(f"查询结转凭证失败: {e}")

    print("\n--- 相似凭证检测 ---")
    # 查找金额接近或相同的凭证
    sim_res = frappe.db.sql("""
        SELECT 
            voucher_no, 
            SUM(debit) as total_debit, 
            COUNT(*) as entries_count,
            creation
        FROM `tabGL Entry` 
        WHERE is_opening = 'Yes' 
        GROUP BY voucher_no
        HAVING total_debit > 23000000
    """, as_dict=True)
    for r in sim_res:
         print(f"大额凭证: {r.voucher_no}, 总借方: {r.total_debit}, 创建时间: {r.creation}")

    print("\n--- 行数对比分析 ---")
    jea_count = frappe.db.count("Journal Entry Account", {"parent": "ACC-JV-2026-05264"})
    gle_count = frappe.db.count("GL Entry", {"voucher_no": "ACC-JV-2026-05264"})
    print(f"凭证明细行数 (Journal Entry Account): {jea_count}")
    print(f"实际会计分录数 (GL Entry): {gle_count}")
    
    if gle_count == jea_count * 2:
        print("结论：GL Entry 数量正好是明细行的 2 倍，确认发生了重复过账。")
    elif gle_count > jea_count:
        print(f"结论：GL Entry 数量多于明细行（多出 {gle_count - jea_count} 行）。")

if __name__ == "__main__":
    frappe.init(site="aierp.local")
    frappe.connect()
    try:
        run()
    finally:
        frappe.destroy()
