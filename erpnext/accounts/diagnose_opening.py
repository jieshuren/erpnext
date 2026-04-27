import frappe

def diagnose():
    print("=" * 80)
    print("期初余额诊断报告")
    print("=" * 80)
    
    pcv_list = frappe.db.sql("""
        SELECT name, period_start_date, period_end_date, docstatus, creation
        FROM `tabPeriod Closing Voucher`
        WHERE docstatus = 1
        ORDER BY period_end_date
    """, as_dict=True)
    
    print("\n【1】Period Closing Voucher (已提交的):")
    if pcv_list:
        for pcv in pcv_list:
            print(f"  - {pcv.name}: {pcv.period_start_date} ~ {pcv.period_end_date} (创建于: {pcv.creation})")
    else:
        print("  无 Period Closing Voucher")
    
    opening_si = frappe.db.sql("""
        SELECT name, posting_date, outstanding_amount
        FROM `tabSales Invoice`
        WHERE is_opening = 'Yes' AND docstatus = 1
        ORDER BY posting_date
    """, as_dict=True)
    
    opening_pi = frappe.db.sql("""
        SELECT name, posting_date, outstanding_amount
        FROM `tabPurchase Invoice`
        WHERE is_opening = 'Yes' AND docstatus = 1
        ORDER BY posting_date
    """, as_dict=True)
    
    opening_invoices = opening_si + opening_pi
    
    print(f"\n【2】Opening Invoice (已提交): {len(opening_invoices)} 条")
    if opening_invoices:
        for inv in opening_invoices[:5]:
            print(f"  - {inv.name}: {inv.posting_date}, 金额: {inv.outstanding_amount}")
        if len(opening_invoices) > 5:
            print(f"  ... 还有 {len(opening_invoices) - 5} 条")
    
    total_gle_cnt = frappe.db.sql("""
        SELECT COUNT(*) as cnt
        FROM `tabGL Entry`
        WHERE is_opening = 'Yes' AND is_cancelled = 0
    """, as_dict=True)[0].cnt
    
    print(f"\n【3】GL Entry (is_opening='Yes', 总记录数): {total_gle_cnt}")
    
    print(f"\n【3.5】GL Entry 总览 (按 is_opening 分组):")
    gle_overview = frappe.db.sql("""
        SELECT is_opening, 
               COUNT(*) as cnt,
               SUM(debit) as total_debit,
               SUM(credit) as total_credit
        FROM `tabGL Entry`
        WHERE is_cancelled = 0
        GROUP BY is_opening
    """, as_dict=True)
    for row in gle_overview:
        print(f"  is_opening={row.is_opening}: {row.cnt} 条, 借方: {row.total_debit:,.2f}, 贷方: {row.total_credit:,.2f}")
    
    print(f"\n【3.6】检查最早的 GL Entry 日期:")
    earliest_gle = frappe.db.sql("""
        SELECT MIN(posting_date) as earliest, MAX(posting_date) as latest
        FROM `tabGL Entry`
        WHERE is_cancelled = 0
    """, as_dict=True)[0]
    print(f"  最早日期: {earliest_gle.earliest}")
    print(f"  最晚日期: {earliest_gle.latest}")
    
    print(f"\n【3.7】查看最早期的10条 GL Entry:")
    earliest_entries = frappe.db.sql("""
        SELECT posting_date, account, debit, credit, voucher_type, voucher_no
        FROM `tabGL Entry`
        WHERE is_cancelled = 0
        ORDER BY posting_date ASC, creation ASC
        LIMIT 10
    """, as_dict=True)
    for entry in earliest_entries:
        print(f"  - {entry.posting_date} {entry.account}: 借={entry.debit:,.2f}, 贷={entry.credit:,.2f} [{entry.voucher_type}/{entry.voucher_no}]")
    
    print(f"\n【3.8】查看所有 GL Entry 日期分布:")
    date_dist = frappe.db.sql("""
        SELECT posting_date, COUNT(*) as cnt, SUM(debit) as total_debit, SUM(credit) as total_credit
        FROM `tabGL Entry`
        WHERE is_cancelled = 0
        GROUP BY posting_date
        ORDER BY posting_date ASC
        LIMIT 20
    """, as_dict=True)
    for d in date_dist:
        print(f"  - {d.posting_date}: {d.cnt} 条, 借: {d.total_debit:,.2f}, 贷: {d.total_credit:,.2f}")
    
    opening_gle = frappe.db.sql("""
        SELECT COUNT(*) as cnt,
               SUM(debit) as total_debit,
               SUM(credit) as total_credit,
               voucher_type,
               voucher_no
        FROM `tabGL Entry`
        WHERE is_opening = 'Yes' AND is_cancelled = 0
        GROUP BY voucher_type, voucher_no
        ORDER BY SUM(debit) + SUM(credit) DESC
        LIMIT 20
    """, as_dict=True)
    
    if opening_gle:
        for gle in opening_gle:
            print(f"  - {gle.voucher_type}/{gle.voucher_no}: {gle.cnt} 条, 借方: {gle.total_debit:,.2f}, 贷方: {gle.total_credit:,.2f}")
    
    closing_balance_cnt = frappe.db.sql("""
        SELECT COUNT(*) as cnt
        FROM `tabAccount Closing Balance`
    """, as_dict=True)[0].cnt
    
    print(f"\n【4】Account Closing Balance: {closing_balance_cnt} 条记录")
    
    print(f"\n【5】科目期初余额详情 (前10个科目):")
    top_accounts = frappe.db.sql("""
        SELECT account,
               SUM(debit) as total_debit,
               SUM(credit) as total_credit,
               SUM(debit - credit) as net_balance
        FROM `tabGL Entry`
        WHERE is_opening = 'Yes' AND is_cancelled = 0
        GROUP BY account
        ORDER BY ABS(SUM(debit - credit)) DESC
        LIMIT 10
    """, as_dict=True)
    
    for acc in top_accounts:
        print(f"  - {acc.account}:")
        print(f"    借方: {acc.total_debit:>15,.2f}")
        print(f"    贷方: {acc.total_credit:>15,.2f}")
        print(f"    净额: {acc.net_balance:>15,.2f}")
        
        sources = frappe.db.sql("""
            SELECT voucher_type, voucher_no, 
                   SUM(debit) as debit, 
                   SUM(credit) as credit,
                   COUNT(*) as cnt
            FROM `tabGL Entry`
            WHERE account = %s AND is_opening = 'Yes' AND is_cancelled = 0
            GROUP BY voucher_type, voucher_no
        """, acc.account, as_dict=True)
        
        for src in sources[:5]:
            print(f"    来自 {src.voucher_type}/{src.voucher_no}: {src.cnt} 条, 借: {src.debit:,.2f}, 贷: {src.credit:,.2f}")
    
    print(f"\n【6】检查重复导入:")
    
    je_opening = frappe.db.sql("""
        SELECT jv.name, jv.posting_date, jv.total_debit, jv.voucher_type,
               (SELECT COUNT(*) FROM `tabGL Entry` WHERE voucher_type = jv.voucher_type AND voucher_no = jv.name AND is_opening = 'Yes') as gle_cnt
        FROM `tabJournal Entry` jv
        WHERE jv.docstatus = 1
        AND (jv.voucher_type = 'Opening Entry' OR jv.is_opening = 'Yes')
        ORDER BY jv.posting_date DESC
        LIMIT 10
    """, as_dict=True)
    
    if je_opening:
        print(f"  包含 Opening 的 Journal Entry: {len(je_opening)} 条")
        for je in je_opening:
            print(f"    - {je.name}: {je.posting_date}, 金额: {je.total_debit:,.2f}, 类型: {je.voucher_type}, GLE 条数: {je.gle_cnt}")
    
    # 额外检查：查看 2025-02-05 日期的重复数据
    print(f"\n【8】检查最早日期(2025-02-05)的详细数据:")
    earliest_date_entries = frappe.db.sql("""
        SELECT posting_date, account, debit, credit, voucher_type, voucher_no, remarks
        FROM `tabGL Entry`
        WHERE is_cancelled = 0 AND posting_date = '2025-02-05'
        ORDER BY account, debit DESC, credit DESC
    """, as_dict=True)
    for entry in earliest_date_entries:
        print(f"  - {entry.account}: 借={entry.debit:>12,.2f}, 贷={entry.credit:>12,.2f} [{entry.voucher_no}] remarks={entry.remarks}")
    
    # 检查重复 GL Entry
    print(f"\n【11】检查重复的 GL Entry（同一个凭证出现多次）:")
    duplicate_gle = frappe.db.sql("""
        SELECT voucher_type, voucher_no, account, debit, credit, COUNT(*) as cnt, GROUP_CONCAT(name) as names
        FROM `tabGL Entry`
        WHERE is_cancelled = 0
        GROUP BY voucher_type, voucher_no, account, debit, credit
        HAVING COUNT(*) > 1
        ORDER BY cnt DESC
        LIMIT 20
    """, as_dict=True)
    
    if duplicate_gle:
        print(f"  找到 {len(duplicate_gle)} 个重复的 GL Entry:")
        for d in duplicate_gle:
            print(f"    - {d.voucher_no} / {d.account}: 借={d.debit:,.2f}, 贷={d.credit:,.2f}, 重复次数={d.cnt}, 记录ID: {d.names}")
    else:
        print("  没有发现重复的 GL Entry")
    
    # 统计总重复数
    total_duplicates_result = frappe.db.sql("""
        SELECT SUM(cnt - 1) as extra_records
        FROM (
            SELECT COUNT(*) as cnt
            FROM `tabGL Entry`
            WHERE is_cancelled = 0
            GROUP BY voucher_type, voucher_no, account, debit, credit
            HAVING COUNT(*) > 1
        ) t
    """, as_dict=True)
    
    total_duplicates = total_duplicates_result[0].extra_records if total_duplicates_result else 0
    total_gle = frappe.db.sql("SELECT COUNT(*) as cnt FROM `tabGL Entry` WHERE is_cancelled = 0", as_dict=True)[0].cnt
    
    print(f"\n  总 GL Entry 记录数: {total_gle} 条")
    print(f"  重复的额外记录数: {total_duplicates} 条")
    print(f"  重复率: {total_duplicates/total_gle*100:.1f}%")
    
    # 检查最早日期的具体凭证
    print(f"\n【12】查看 2025-02-05 的所有不同凭证:")
    vouchers_on_date = frappe.db.sql("""
        SELECT DISTINCT voucher_no, COUNT(*) as entry_count
        FROM `tabGL Entry`
        WHERE is_cancelled = 0 AND posting_date = '2025-02-05'
        GROUP BY voucher_no
        ORDER BY voucher_no
    """, as_dict=True)
    for v in vouchers_on_date:
        print(f"  - {v.voucher_no}: {v.entry_count} 条 GL Entry")
    
    # 检查科目余额（计算值）
    print(f"\n【10】科目余额汇总 (前10个):")
    account_balances = frappe.db.sql("""
        SELECT account, 
               SUM(debit) as total_debit,
               SUM(credit) as total_credit,
               SUM(debit - credit) as net_balance
        FROM `tabGL Entry`
        WHERE is_cancelled = 0
        GROUP BY account
        HAVING ABS(SUM(debit - credit)) > 0
        ORDER BY ABS(SUM(debit - credit)) DESC
        LIMIT 10
    """, as_dict=True)
    for acc in account_balances:
        print(f"  - {acc.account}: 借={acc.total_debit:>15,.2f}, 贷={acc.total_credit:>15,.2f}, 净={acc.net_balance:>15,.2f}")
    all_je = frappe.db.sql("""
        SELECT name, posting_date, voucher_type, is_opening, total_debit
        FROM `tabJournal Entry`
        WHERE docstatus = 1
        ORDER BY posting_date ASC
        LIMIT 20
    """, as_dict=True)
    for je in all_je:
        print(f"  - {je.name}: {je.posting_date}, 类型={je.voucher_type}, is_opening={je.is_opening}, 金额={je.total_debit:,.2f}")
    
    print("\n" + "=" * 80)
    print("诊断完成")
    print("=" * 80)
