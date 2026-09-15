import sqlite3

conn = sqlite3.connect('cms.db')
cur = conn.cursor()

with open('db_results.txt', 'w', encoding='utf-8') as f:
    tables = cur.execute('SELECT name FROM sqlite_master WHERE type="table"').fetchall()
    for t in tables:
        rows = cur.execute(f'SELECT * FROM {t[0]}').fetchall()
        for row in rows:
            row_str = str(row).lower()
            if 'kamu eti' in row_str or 'liderlik' in row_str or 'yonetim' in row_str or 'yönetim' in row_str or 'hadis' in row_str:
                f.write(t[0] + ' ' + str(row)[:200] + '\n')
