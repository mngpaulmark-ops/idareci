import psycopg2
conn = psycopg2.connect('postgresql://neondb_owner:npg_PHdtr61ILkWz@ep-restless-feather-b25l03vt-pooler.c-6.eu-central-1.aws.neon.tech/neondb?sslmode=require')
cur = conn.cursor()
cur.execute("SELECT key, value FROM setting")
print('Settings in Neon:', cur.fetchall())
