import os
import sqlite3

term = 'tuncer'
db_path = 'cms.db'

# Search in files
print("--- SEARCH IN FILES ---")
for root, dirs, files in os.walk('.'):
    if '.git' in root or '__pycache__' in root or 'venv' in root:
        continue
    for file in files:
        if file.endswith(('.html', '.py', '.txt', '.js', '.css', '.md')):
            path = os.path.join(root, file)
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    for i, line in enumerate(f):
                        if term in line.lower():
                            print(f"{path}:{i+1}: {line.strip()[:100]}")
            except Exception as e:
                pass

# Search in Database
print("\n--- SEARCH IN DATABASE ---")
try:
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [t[0] for t in c.fetchall()]
    
    for table in tables:
        c.execute(f"PRAGMA table_info({table})")
        columns = [col[1] for col in c.fetchall()]
        
        for col in columns:
            try:
                c.execute(f"SELECT * FROM {table} WHERE {col} LIKE ?", ('%'+term+'%',))
                rows = c.fetchall()
                for row in rows:
                    print(f"Table: {table}, Column: {col}, Data: {row}")
            except:
                pass
except Exception as e:
    print("DB error:", e)
