import sqlite3
c=sqlite3.connect('instance/cms.db').cursor()
print(c.execute("SELECT * FROM pragma_table_info('haber')").fetchall())
