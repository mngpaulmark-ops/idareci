import sqlite3
import re
from datetime import datetime

# 1. Create table if not exists
conn = sqlite3.connect('cms.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS etkinlik (
        id INTEGER PRIMARY KEY,
        edate VARCHAR(20),
        saat VARCHAR(10),
        type VARCHAR(50),
        title VARCHAR(200),
        description TEXT,
        link VARCHAR(255)
    )
''')

# 2. Parse the SQL string to insert events
sql_content = """INSERT INTO `burokratlar_etkinlik` (`id`, `ordernum`, `edate`, `type`, `title`, `description`, `link`, `color`, `adres`, `saat`) VALUES (1,1457179200,1457179200,'meeting','28 ŞUBAT YAŞAYAN BİRİ','GENÇ BİR BAKIŞ AÇISIYLA 28 ŞUBAT BU HAFTAKİ KONFERANS KONUMUZ VE KONUŞUMUZ 54. HÜKÜMETİN DEVLET BAKANI VE AK PARTİ ETİK KURULU BAŞKANI SAYIN AHMET CEMİL TUNÇ','#','','GMK Bulvarı No:36/19 Demirtepe / ANKARA','14:00'),(2,0,1457775936,'meeting','MİLLET ANAYASASINA','Dost meclisinin bu haftaki konuğu Cumhurbaşkanı Başdanışmanı Sayın Av. Şeref Malkoç Katılacaktır.','#','','GMK Bulvarı No:36/19 Demirtepe / ANKARA','14:00'),(10,0,1460228400,NULL,'SULTAN II ABDÜLHAMİD''DEN RECEP TAYYİP ERDOĞAN''A','BU KONFERANS ÇOK KONUŞULACAK.  Sultan Abdülhamit''e ait bilinmeyenler,','','','Yer:İdareci ve Bürokratlar  Birliği Derneği  GMK  Bulvarı No:36/19  Demirtepe/ANKARA',''),(18,0,1463097600,NULL,' PKK Medyası ve PKK İle Mücadelenin psikolojik Boyutu','Bu tarihi lüten not ediniz...Pkk...Sistematik dezenformasyon ve Pkk...Pkknın kara propagandası...Pkknın medyayı kullanma araçları...Pkkya destek veren Avrupa ülkeleri...Daha neler neler...','','','Yer: İdareci  ve Bürokratlar  Birliği  Derneği   GMK  Bulvarı  No:36/19  Demirtepe/ANKARA',''),(17,0,1459364400,NULL,'Terör,  Göç ve Dokunulmazlık','ŞİMDİDEN BU TARİHİ VE SAATİ NOT EDIN...Terörün gerçek yüzü nedir, hedefi kimdir?Terör örgütleri ve hamileri kimlerdir?Terör örgütünün iç ve dış bağlantıları...Neden terör daha çok belli bir coğrafyadadır?Terörün zararaları, tehlikeleri, etkileri, bilinmeyenleri....Teröre dair daha neler neler...Göç...Göç ve terörün bağlantıları...Göç sosyolojidi ve psikolojisi...İç ve dış göç...Dokunulmazlıklar...Dokunulmazlıkların ölçüsü, sınırı, bağlantıları...Terör, göç ve dokunulmazlıkların bağlantı ve ilişkileri..&nbsp;Batı ve Dünyanın bakışı, samimiyeti, etkisi......Ve daha neler neler...','#','','İdareci ve Bürokratlar Birliği Derneği GMK  Bulvarı No:36/19  Demirtepe ANKARA',''),(19,0,1464307200,NULL,'Küresel Meydan Okumalar ve Tükiye''nin Dış Politikası','Dost Meclisimizin Bu haftaki Konuğu STAR Gazetesi Ankara Temsilcisi olan Sayın Mustafa KARTOĞLU bey ile “Küresel Meydan Okumalar ve Tükiye''nin Dış Politikası" İsimli Konferansı siz değerli konuklarımız ile buluşturmaktadır. ','','','İdareci ve Bürokratlar Birliği Derneği  GMK  Bulvarı No:36/19  Demirtepe/ANKARA',''),(20,0,1533682800,NULL,'Olağanüstü Kongre Kararı','YK. Kurulumuz Toplanarak almış olduğu Olağanüstü Kongre kararı doğrulturunsa 08.08.2018&nbsp;tarihinde&nbsp;toplanmasına, 06.08.2018 tarihinde ÇOĞUNLUK ARANMAKSINIZ 16.08.2018 Perşembe Saat 19.00''da İDARECİ ve BÜROKRATLAR BİRLİĞİ DERNEĞİNDE OLAĞAN ÜSTÜ KONGRE yapılacaktır.&nbsp;','','','İBB-DER Genel Mekrezi',''),(21,0,1534377600,NULL,'Olağanüstü Kongre Kararı','Olağanüstü Kongremiz 16.08.2018 Perşembe günü saat 19.00''da NEFF CAFE-NEFFGÜLE Toplantı Salonunda yapılacaktır.( Atatürk Caddesi. Keçiören Girişi FTZ Arkası No:17 Keçiören-ANKARA) Teşriflerinizi bekler,Kongremizin; Derneğimize, Vatanımıza, İslam Alemine ve İnsanlığa hayırlı olmasını temenni ederiz.Yücel CAN','','','Atatürk Caddesi. Keçiören Girişi FTZ Arkası No:17 Keçiören-ANKARA',''),(22,0,1747094400,NULL,'13.5.2025 Dost Meclisi Buluşması Ankara Devlet Türk Halk Müziği  18 Mart Çanakkale Zaferi ve Biz Birlikte Güçlüyüz Ruhu İle Kahramanlık Eserleri Programı','13.5.2025 Dost Meclisi Buluşması Ankara Devlet Türk Halk Müziği  18 Mart Çanakkale Zaferi ve Biz Birlikte Güçlüyüz Ruhu İle Kahramanlık Eserleri Programına  Teşriflerinizden Mutluluk Duyarız','','','',''),(23,0,1747162800,NULL,'13.5.2025 Dost Meclisi Buluşması Ankara Devlet Türk Halk Müziği  18 Mart Çanakkale Zaferi ve Biz Birlikte Güçlüyüz Ruhu İle Kahramanlık Eserleri Programı','13.5.2025 Dost Meclisi Buluşması Ankara Devlet Türk Halk Müziği  18 Mart Çanakkale Zaferi ve Biz Birlikte Güçlüyüz Ruhu İle Kahramanlık Eserleri Programına Teşriflerinizden Mutluluk Duyarız','','','Ulus-Hamam Önü- Kabakçı Konağı','');"""

# It's easier to just parse the known 10 records directly since I have the Turkish correctly encoded text in my own thought block!
events = [
    (1, "1457179200", "14:00", "meeting", "28 ŞUBAT YAŞAYAN BİRİ", "GENÇ BİR BAKIŞ AÇISIYLA 28 ŞUBAT BU HAFTAKİ KONFERANS KONUMUZ VE KONUŞUMUZ 54. HÜKÜMETİN DEVLET BAKANI VE AK PARTİ ETİK KURULU BAŞKANI SAYIN AHMET CEMİL TUNÇ", "#"),
    (2, "1457775936", "14:00", "meeting", "MİLLET ANAYASASINA", "Dost meclisinin bu haftaki konuğu Cumhurbaşkanı Başdanışmanı Sayın Av. Şeref Malkoç Katılacaktır.", "#"),
    (10, "1460228400", "", "", "SULTAN II ABDÜLHAMİD'DEN RECEP TAYYİP ERDOĞAN'A", "BU KONFERANS ÇOK KONUŞULACAK. Sultan Abdülhamit'e ait bilinmeyenler,", ""),
    (18, "1463097600", "", "", "PKK Medyası ve PKK İle Mücadelenin psikolojik Boyutu", "Bu tarihi lüten not ediniz...Pkk...Sistematik dezenformasyon ve Pkk...Pkknın kara propagandası...Pkknın medyayı kullanma araçları...Pkkya destek veren Avrupa ülkeleri...Daha neler neler...", ""),
    (17, "1459364400", "", "", "Terör, Göç ve Dokunulmazlık", "ŞİMDİDEN BU TARİHİ VE SAATİ NOT EDIN...Terörün gerçek yüzü nedir, hedefi kimdir?Terör örgütleri ve hamileri kimlerdir?Terör örgütünün iç ve dış bağlantıları...Neden terör daha çok belli bir coğrafyadadır?Terörün zararaları, tehlikeleri, etkileri, bilinmeyenleri....Teröre dair daha neler neler...Göç...Göç ve terörün bağlantıları...Göç sosyolojidi ve psikolojisi...İç ve dış göç...Dokunulmazlıklar...Dokunulmazlıkların ölçüsü, sınırı, bağlantıları...Terör, göç ve dokunulmazlıkların bağlantı ve ilişkileri..&nbsp;Batı ve Dünyanın bakışı, samimiyeti, etkisi......Ve daha neler neler...", "#"),
    (19, "1464307200", "", "", "Küresel Meydan Okumalar ve Tükiye'nin Dış Politikası", "Dost Meclisimizin Bu haftaki Konuğu STAR Gazetesi Ankara Temsilcisi olan Sayın Mustafa KARTOĞLU bey ile “Küresel Meydan Okumalar ve Tükiye'nin Dış Politikası\" İsimli Konferansı siz değerli konuklarımız ile buluşturmaktadır. ", ""),
    (20, "1533682800", "", "", "Olağanüstü Kongre Kararı", "YK. Kurulumuz Toplanarak almış olduğu Olağanüstü Kongre kararı doğrulturunsa 08.08.2018&nbsp;tarihinde&nbsp;toplanmasına, 06.08.2018 tarihinde ÇOĞUNLUK ARANMAKSINIZ 16.08.2018 Perşembe Saat 19.00'da İDARECİ ve BÜROKRATLAR BİRLİĞİ DERNEĞİNDE OLAĞAN ÜSTÜ KONGRE yapılacaktır.&nbsp;", ""),
    (21, "1534377600", "", "", "Olağanüstü Kongre Kararı", "Olağanüstü Kongremiz 16.08.2018 Perşembe günü saat 19.00'da NEFF CAFE-NEFFGÜLE Toplantı Salonunda yapılacaktır.( Atatürk Caddesi. Keçiören Girişi FTZ Arkası No:17 Keçiören-ANKARA) Teşriflerinizi bekler,Kongremizin; Derneğimize, Vatanımıza, İslam Alemine ve İnsanlığa hayırlı olmasını temenni ederiz.Yücel CAN", ""),
    (22, "1747094400", "", "", "13.5.2025 Dost Meclisi Buluşması Ankara Devlet Türk Halk Müziği 18 Mart Çanakkale Zaferi ve Biz Birlikte Güçlüyüz Ruhu İle Kahramanlık Eserleri Programı", "13.5.2025 Dost Meclisi Buluşması Ankara Devlet Türk Halk Müziği 18 Mart Çanakkale Zaferi ve Biz Birlikte Güçlüyüz Ruhu İle Kahramanlık Eserleri Programına Teşriflerinizden Mutluluk Duyarız", ""),
    (23, "1747162800", "", "", "13.5.2025 Dost Meclisi Buluşması Ankara Devlet Türk Halk Müziği 18 Mart Çanakkale Zaferi ve Biz Birlikte Güçlüyüz Ruhu İle Kahramanlık Eserleri Programı", "13.5.2025 Dost Meclisi Buluşması Ankara Devlet Türk Halk Müziği 18 Mart Çanakkale Zaferi ve Biz Birlikte Güçlüyüz Ruhu İle Kahramanlık Eserleri Programına Teşriflerinizden Mutluluk Duyarız", "")
]

for ev in events:
    # Convert UNIX timestamp to DD.MM.YYYY string
    dt = datetime.fromtimestamp(int(ev[1])).strftime('%d.%m.%Y')
    c.execute("INSERT OR REPLACE INTO etkinlik (id, edate, saat, type, title, description, link) VALUES (?, ?, ?, ?, ?, ?, ?)", 
              (ev[0], dt, ev[2], ev[3], ev[4], ev[5], ev[6]))

conn.commit()
conn.close()
print("Imported Etkinlikler into database!")
