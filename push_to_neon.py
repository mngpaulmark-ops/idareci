import sqlite3
import psycopg2

neon_url = 'postgres://neondb_owner:npg_PHdtr61ILkWz@ep-restless-feather-b25l03vt-pooler.c-6.eu-central-1.aws.neon.tech/neondb?sslmode=require'
sqlite_path = 'instance/cms.db'

print('Connecting to SQLite...')
sl_conn = sqlite3.connect(sqlite_path)
sl_conn.row_factory = sqlite3.Row
sl_cur = sl_conn.cursor()

print('Connecting to Neon PostgreSQL...')
pg_conn = psycopg2.connect(neon_url)
pg_cur = pg_conn.cursor()

sl_cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [r['name'] for r in sl_cur.fetchall()]

for table in tables:
    if table == 'sqlite_sequence': continue
    print(f'Copying table: {table}')
    sl_cur.execute(f'SELECT * FROM {table}')
    rows = sl_cur.fetchall()
    if not rows: continue
    
    cols = rows[0].keys()
    col_str = ', '.join([f'"{c}"' for c in cols])
    placeholders = ', '.join(['%s' for _ in cols])
    
    pg_cur.execute(f'TRUNCATE TABLE "{table}" CASCADE;')
    insert_query = f'INSERT INTO "{table}" ({col_str}) VALUES ({placeholders})'
    data_to_insert = [tuple(r) for r in rows]
    
    try:
        from psycopg2.extras import execute_batch
        execute_batch(pg_cur, insert_query, data_to_insert)
        print(f' -> Copied {len(data_to_insert)} rows.')
    except Exception as e:
        print(f' -> Error copying {table}: {e}')
        pg_conn.rollback()
        continue
        
pg_conn.commit()
print('Migration complete!')
