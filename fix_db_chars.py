import sqlite3

conn = sqlite3.connect('instance/cms.db')
c = conn.cursor()

menu_fixes = {
    2: '➣ Derneğimiz',
    3: 'Hakkımızda',
    4: 'Tüzüğümüz',
    5: 'Yönetim Kurulu',
    6: 'Başkanlık ve Birimler',
    7: 'Yüksek İstişare ve Onur Kurulu',
    8: 'Diğer Kurullar',
    10: 'Üyelerimiz',
    14: 'Fotoğraf Galerisi',
    17: 'İletişim'
}

for _id, title in menu_fixes.items():
    c.execute('UPDATE menu SET title=? WHERE id=?', (title, _id))

left_menu_fixes = {
    1: '➣ Hakkımızda',
    2: '➣ Yönetim Kurulu',
    3: '➣ Başkanlık ve Birimler',
    4: '➣ Projeler',
    5: '➣ Yüksek İstişare ve Onur Kurulu',
    6: '➣ Diğer Kurullar',
    7: '➣ Temsilcilikler',
    8: '➣ Gençlik Kolları',
    9: '➣ Üyelerimiz',
    10: '➣ Haberler',
    11: '➣ Duyurular',
    12: '➣ Etkinlikler',
    13: '➣ Raporlar / Belgeler'
}

for _id, title in left_menu_fixes.items():
    c.execute('UPDATE left_menu SET title=? WHERE id=?', (title, _id))

yazar_fixes = {
    1: 'Yücel CAN',
    3: 'Prof. Dr. Mutlu TÜRKMEN',
    4: 'Doç. Dr. Taner BOZKUŞ',
    5: 'Mehmet MEMDOĞLU',
    8: 'Prof.Dr. Aliye M. Aktaş',
    9: 'Mehmet ŞAN',
    10: 'Dr. Ahmet Naci DİLEK',
    11: 'Ahmet ÖZYANIK',
    12: 'Mehmet AVŞAR',
    13: 'Dr. İmbat MUĞLU',
    14: 'İsmail AKGÜN',
    15: '28-9-2024 Yücel Can Başyazar: BİRLİKTE GÜÇLÜ BİR ŞEKİLDE GELENEKTEN GELECEĞE - Haberin Saati - Haberin Saati'
}

for _id, name in yazar_fixes.items():
    c.execute('UPDATE yazar SET name=? WHERE id=?', (name, _id))

    
conn.commit()
conn.close()
print("Fixed menus!")
