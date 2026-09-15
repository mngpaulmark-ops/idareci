import sqlite3

def add_side_links():
    conn = sqlite3.connect('cms.db')
    c = conn.cursor()
    # Ensure table exists
    c.execute('''CREATE TABLE IF NOT EXISTS side_link (
        id INTEGER PRIMARY KEY,
        category VARCHAR(50),
        title VARCHAR(255),
        url VARCHAR(255),
        badge VARCHAR(100),
        `order` INTEGER,
        is_active BOOLEAN
    )''')
    
    # Check if we already have data
    c.execute('SELECT COUNT(*) FROM side_link')
    count = c.fetchone()[0]
    
    if count == 0:
        links = [
            # Dijital
            ('dijital', 'Üyelik Başvurusu', 'uyelik.html', '#800000', 1, True),
            ('dijital', 'Aidat Sorgulama', '#', '#e2e8f0', 2, True),
            
            # Gündem
            ('gundem', 'Politika Notu Yayını', '#', 'Yakında', 1, True),
            ('gundem', 'Dost Meclisi Buluşması', '#', '14 Mayıs', 2, True),
            
            # Faydalı
            ('faydali', 'Cumhurbaşkanlığı', 'https://www.tccb.gov.tr/', '', 1, True),
            ('faydali', 'Türkiye Büyük Millet Meclisi', 'https://www.tbmm.gov.tr/', '', 2, True),
            ('faydali', 'E-devlet', 'https://www.turkiye.gov.tr/', '', 3, True),
            ('faydali', 'T.C. İçişleri Bakanlığı', 'https://www.icisleri.gov.tr/', '', 4, True),
            ('faydali', 'Resmin Gazete', 'https://www.resmigazete.gov.tr/', '', 5, True),
            ('faydali', 'Cumhurbaşkanlığı İ.M. (CİMER)', 'https://www.cimer.gov.tr/', '', 6, True),
            
            # E-Bulten (just to toggle the block itself, no list)
            ('ebulten', 'E-Bülten & Politika Notlarına Abone Olun', '', '', 1, True)
        ]
        
        c.executemany('INSERT INTO side_link (category, title, url, badge, `order`, is_active) VALUES (?, ?, ?, ?, ?, ?)', links)
        conn.commit()
    conn.close()

if __name__ == '__main__':
    add_side_links()
