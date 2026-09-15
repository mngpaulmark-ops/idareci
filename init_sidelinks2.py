import sqlite3
import os

db_path = os.path.join('instance', 'cms.db')
conn = sqlite3.connect(db_path)
c = conn.cursor()

c.execute('SELECT COUNT(*) FROM side_link')
count = c.fetchone()[0]
print('Side_link count:', count)

if count == 0:
    links = [
        ('dijital', 'Üyelik Başvurusu', 'uyelik.html', '#800000', 1, 1),
        ('dijital', 'Aidat Sorgulama', '#', '#e2e8f0', 2, 1),
        ('gundem', 'Politika Notu Yayını', '#', 'Yakında', 1, 1),
        ('gundem', 'Dost Meclisi Buluşması', '#', '14 Mayıs', 2, 1),
        ('faydali', 'Cumhurbaşkanlığı', 'https://www.tccb.gov.tr/', '', 1, 1),
        ('faydali', 'Türkiye Büyük Millet Meclisi', 'https://www.tbmm.gov.tr/', '', 2, 1),
        ('faydali', 'E-devlet', 'https://www.turkiye.gov.tr/', '', 3, 1),
        ('faydali', 'T.C. İçişleri Bakanlığı', 'https://www.icisleri.gov.tr/', '', 4, 1),
        ('faydali', 'Resmin Gazete', 'https://www.resmigazete.gov.tr/', '', 5, 1),
        ('faydali', 'Cumhurbaşkanlığı İ.M. (CİMER)', 'https://www.cimer.gov.tr/', '', 6, 1),
        ('ebulten', 'E-Bülten & Politika Notlarına Abone Olun', '', '', 1, 1)
    ]
    
    c.executemany('INSERT INTO side_link (category, title, url, badge, "order", is_active) VALUES (?, ?, ?, ?, ?, ?)', links)
    conn.commit()
    print('Inserted into instance/cms.db')
conn.close()
