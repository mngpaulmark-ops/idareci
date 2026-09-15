from app import app, db, Yonkur
import re

sql_path = r'C:\Users\turga\OneDrive\Desktop\bürokratlar birliği orjinal site yedeği\backup-8.11.2026_11-19-03_burokratlarbirli\backup-8.11.2026_11-19-03_burokratlarbirli\mysql\burokratlarbirli_database.sql'
sql = open(sql_path, encoding='utf-8', errors='ignore').read()

with app.app_context():
    db.create_all()
    # Check if we already migrated
    if Yonkur.query.count() == 0:
        for line in sql.split('\n'):
            if line.startswith('INSERT INTO `burokratlar_yonkur`'):
                pattern = r"\((?P<id>\d+),'(?P<durum>\d+)',(?P<ordernum>\d+),'(?P<grup>[^']*)','(?P<name>.*?)','(?P<unvan>.*?)',"
                matches = re.finditer(pattern, line)
                for m in matches:
                    if m.group('durum') == '1':
                        y = Yonkur()
                        y.id = int(m.group('id'))
                        y.grup = m.group('grup')
                        y.ordernum = int(m.group('ordernum'))
                        y.name = m.group('name').replace('\\\'', '\'')
                        y.unvan = m.group('unvan').replace('\\\'', '\'')
                        y.image_path = f"data/yonkur/{m.group('id')}.jpg"
                        db.session.add(y)
        db.session.commit()
        print('Migrated Yonkur table from SQL backup!')
    else:
        print('Yonkur already has data.')
