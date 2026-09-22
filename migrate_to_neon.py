
import sqlite3
from app import app, db
import psycopg2

def migrate():
    print('Creating tables in Neon PostgreSQL...')
    with app.app_context():
        db.create_all()
        print('Tables created successfully.')

        # Currently we only create tables. Data migration can be added if needed.
        # But wait, local SQLite has news and settings. Let's do a basic data migration.

if __name__ == '__main__':
    migrate()

