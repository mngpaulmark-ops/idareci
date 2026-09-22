import sqlite3
import psycopg2

neon_url = 'postgresql://neondb_owner:npg_PHdtr61ILkWz@ep-restless-feather-b25l03vt-pooler.c-6.eu-central-1.aws.neon.tech/neondb?sslmode=require'
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
    
    # Get columns in Neon
    pg_cur.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table}';")
    neon_cols_info = pg_cur.fetchall()
    if not neon_cols_info:
        print(f'Table {table} not found in Neon. Skipping.')
        continue
    
    neon_cols = [c[0] for c in neon_cols_info]
    neon_col_types = {c[0]: c[1] for c in neon_cols_info}
    
    sl_cur.execute(f'SELECT * FROM {table}')
    rows = sl_cur.fetchall()
    if not rows: continue
    
    # Filter rows to only include columns that exist in Neon
    cols = [c for c in rows[0].keys() if c in neon_cols]
    col_str = ', '.join([f'"{c}"' for c in cols])
    placeholders = ', '.join(['%s' for _ in cols])
    
    pg_cur.execute(f'TRUNCATE TABLE "{table}" CASCADE;')
    insert_query = f'INSERT INTO "{table}" ({col_str}) VALUES ({placeholders})'
    
    data_to_insert = []
    for r in rows:
        row_data = []
        for c in cols:
            val = r[c]
            # Convert integer to boolean if Neon expects boolean
            if neon_col_types[c] == 'boolean':
                val = bool(val)
            if neon_col_types[c] == 'character varying' and isinstance(val, str):
                if len(val) > 100:
                    val = val[:100]
            row_data.append(val)
        data_to_insert.append(tuple(row_data))
    
    try:
        from psycopg2.extras import execute_batch
        execute_batch(pg_cur, insert_query, data_to_insert)
        pg_conn.commit()  # Commit per table!
        print(f' -> Copied {len(data_to_insert)} rows.')
    except Exception as e:
        print(f' -> Error copying {table}: {e}')
        pg_conn.rollback()
        
print('Migration complete!')
