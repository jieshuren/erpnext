import frappe

def deduplicate_gl_entries():
    frappe.connect()
    print("Starting AGGRESSIVE GL DEDUPLICATION...")
    
    # 1. 找出所有重复的分录 ID
    # 我们按业务主键分组，保留每一组中 ID 最小的
    raw_dupes = frappe.db.sql("""
        SELECT GROUP_CONCAT(name) as ids
        FROM `tabGL Entry`
        WHERE posting_date >= '2025-01-01'
        GROUP BY voucher_no, account, debit, credit, posting_date, voucher_detail_no, project, department
        HAVING COUNT(*) > 1
    """, as_dict=True)
    
    all_to_delete = []
    for row in raw_dupes:
        ids = row['ids'].split(',')
        # ids[0] 是最小的，保留；其余的 ids[1:] 全部删掉
        all_to_delete.extend(ids[1:])
    
    if not all_to_delete:
        print("No absolute duplicates found.")
        return

    print(f"Total redundant records to remove: {len(all_to_delete)}")
    
    # 分批删除，防止 SQL 语句过长
    batch_size = 500
    for i in range(0, len(all_to_delete), batch_size):
        batch = all_to_delete[i:i + batch_size]
        frappe.db.sql("DELETE FROM `tabGL Entry` WHERE name IN (%s)" % 
                      ", ".join(["'%s'" % id for id in batch]))
    
    frappe.db.commit()
    print(f"Aggressive cleanup finished.")

if __name__ == "__main__":
    deduplicate_gl_entries()
