import sqlite3
print(sqlite3.connect('instance/cms.db').execute('SELECT name FROM sqlite_master WHERE type="table"').fetchall())
