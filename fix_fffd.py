import os
import bs4
import sqlite3

def fix_fffd(html):
    rep = {
        '\ufffdUBAT': 'ŞUBAT',
        '\ufffdYA\ufffdAYAN': 'YAŞAYAN',
        'B\ufffdR\ufffd': 'BİRİ',
        'G\ufffdEN\ufffd': 'GENÇ',
        'BAKI\ufffd': 'BAKIŞ',
        'A\ufffdISIYLA': 'AÇISIYLA',
        'HAFTAK\ufffd': 'HAFTAKİ',
        'KONU\ufffdUMUZ': 'KONUĞUMUZ',
        'H\ufffdK\ufffdMET\ufffdN': 'HÜKÜMETİN',
        'D\ufffdevlet': 'Devlet',
        'D\ufffdEVLET': 'DEVLET',
        'PART\ufffd': 'PARTİ',
        'ET\ufffdK': 'ETİK',
        'BA\ufffdKANI': 'BAŞKANI',
        'CEM\ufffdL': 'CEMİL',
        'TUN\ufffd': 'TUNÇ',
        'M\ufffdLLET': 'MİLLET',
        'konu\ufffdu': 'konuğu',
        'Cumhurba\ufffdkan\ufffd': 'Cumhurbaşkanı',
        'Ba\ufffdd\ufffdan\ufffdman\ufffd': 'Başdanışmanı',
        'Say\ufffdn': 'Sayın',
        '\ufffderef': 'Şeref',
        'Malko\ufffd': 'Malkoç',
        'Kat\ufffdlacakt\ufffdr': 'Katılacaktır',
        'ABD\ufffdLHAM\ufffdD': 'ABDÜLHAMİD',
        'TAYY\ufffdP': 'TAYYİP',
        'ERD\ufffdO\ufffdAN': 'ERDOĞAN',
        '\ufffdOK': 'ÇOK',
        'KONU\ufffdULACAK': 'KONUŞULACAK',
        'Medyas\ufffd': 'Medyası',
        '\ufffdle': 'İle',
        'M\ufffdcadelenin': 'Mücadelenin',
        'l\ufffdten': 'lütfen',
        'propagandas\ufffd': 'propagandası',
        'ara\ufffdlar\ufffd': 'araçları',
        '\ufffdlkeleri': 'ülkeleri',
        'Ter\ufffdr': 'Terör',
        'G\ufffd\ufffd': 'Göç',
        '\ufffdMD\ufffdD\ufffdEN': 'ŞİMDİDEN',
        'TAR\ufffdH\ufffd': 'TARİHİ',
        'SAAT\ufffd': 'SAATİ',
        'ger\ufffdek': 'gerçek',
        'y\ufffdz\ufffd': 'yüzü',
        '\ufffdrg\ufffdt\ufffdleri\ufffd': 'örgütleri',
        '\ufffdrg\ufffdt\ufffdn\ufffdn': 'örgütünün',
        'i\ufffd': 'iç',
        'd\ufffd\ufffd': 'dış',
        'ba\ufffdlant\ufffdlar\ufffd': 'bağlantıları',
        '\ufffdok': 'çok',
        'co\ufffdrafyadad\ufffdr': 'coğrafyadadır',
        'zararalar\ufffd': 'zararları',
        's\ufffdn\ufffdr\ufffd': 'sınırı',
        'ili\ufffdkileri': 'ilişkileri',
        'bak\ufffd\ufffd\ufffd': 'bakışı',
        'K\ufffdresel': 'Küresel',
        'T\ufffdrkiye': 'Türkiye',
        'D\ufffd\ufffd': 'Dış',
        'Politikas\ufffd': 'Politikası',
        'KARTO\ufffdLU': 'KARTOĞLU',
        'bulu\ufffdturmaktad\ufffdr': 'buluşturmaktadır',
        'Ola\ufffdan\ufffdst\ufffd': 'Olağanüstü',
        'alm\ufffd\ufffd': 'almış',
        'oldu\ufffdu': 'olduğu',
        'do\ufffdrulturunsa': 'doğrultusunda',
        'toplanmas\ufffdna': 'toplanmasına',
        '\ufffdO\ufffdUNLUK': 'ÇOĞUNLUK',
        'Per\ufffdembe': 'Perşembe',
        '\ufffdDAREC\ufffd': 'İDARECİ',
        'B\ufffdRL\ufffd\ufffd\ufffd': 'BİRLİĞİ',
        'D\ufffdERNE\ufffd\ufffdND\ufffdE': 'DERNEĞİNDE',
        'OLA\ufffdAN \ufffdST\ufffd': 'OLAĞANÜSTÜ',
        'yap\ufffdlacakt\ufffdr': 'yapılacaktır',
        'g\ufffdn\ufffd': 'günü',
        'G\ufffdLE': 'GÜLE',
        'Ke\ufffdi\ufffdren': 'Keçiören',
        'Giri\ufffdi': 'Girişi',
        'Te\ufffdri\ufffdflerinizi': 'Teşriflerinizi',
        'Derne\ufffdimize': 'Derneğimize',
        'Vatan\ufffdm\ufffdza': 'Vatanımıza',
        '\ufffdslam': 'İslam',
        '\ufffdnsanl\ufffd\ufffda': 'İnsanlığa',
        'hay\ufffdrl\ufffd': 'hayırlı',
        'olmas\ufffdn\ufffd': 'olmasını',
        'Y\ufffdcel': 'Yücel',
        'Bulvar\ufffd': 'Bulvarı',
        '\ufffddareci\ufffd': 'İdareci',
        'B\ufffdr\ufffdokratlar': 'Bürokratlar',
        'Bi\ufffdrli\ufffdi\ufffd': 'Birliği',
        'D\ufffderne\ufffdi\ufffd': 'Derneği',
        '\ufffd\ufffdlemler': 'İşlemler',
        'A\ufffdklama': 'Açıklama',
        'Tari\ufffdh': 'Tarih',
        'D\ufffdokunulmazl\ufffdk': 'Dokunulmazlık',
        'dokunulmazl\ufffdklar\ufffdn': 'dokunulmazlıkların',
        'bi\ufffdli\ufffdnmeyen\ufffdler': 'bilinmeyenler',
        'G\ufffdMK': 'GMK',
        'D\ufffdemi\ufffdrtepe': 'Demirtepe',
        'ned\ufffdi\ufffdr': 'nedir',
        'hed\ufffdefi\ufffd': 'hedefi',
        'ki\ufffcmd\ufffdi\ufffdr': 'kimdir',
        'ed\ufffdin': 'edin',
        'ai\ufffdt': 'ait',
        'dezanformasyon': 'dezenformasyon',
        'bi\ufffdli\ufffdnmeyen\ufffdleri\ufffd': 'bilinmeyenleri',
        'A\ufffdklama': 'Açıklama',
        'G\ufffdEN\ufffd': 'GENÇ',
        'D\ufffdEVLET': 'DEVLET',
        'mecli\ufffdsi\ufffdni\ufffdn': 'meclisinin',
        'Abd\ufffdlhami\ufffdt': 'Abdülhamit',
        '\ufffdrg\ufffdt\ufffdleri\ufffd': 'örgütleri',
        '\ufffddareci': 'İdareci'
    }
    
    for k, v in rep.items():
        html = html.replace(k, v)
    return html

path = os.path.join(r'C:\Users\turga\OneDrive\Desktop\bürokratlar birliği site yedeği\burokratlarbirligi.org', 'etkinlik.html')
with open(path, 'r', encoding='utf-8', errors='surrogateescape') as f:
    local_html = f.read()

fixed_html = fix_fffd(local_html)

# Clean up generic \ufffd that remain
fixed_html = fixed_html.replace('\ufffd', '')

with open(path, 'w', encoding='utf-8', errors='surrogateescape') as f:
    f.write(fixed_html)
    
path_ler = os.path.join(r'C:\Users\turga\OneDrive\Desktop\bürokratlar birliği site yedeği\burokratlarbirligi.org', 'etkinlikler.html')
with open(path_ler, 'w', encoding='utf-8', errors='surrogateescape') as f:
    f.write(fixed_html)

soup = bs4.BeautifulSoup(fixed_html, 'html.parser')
main_div = soup.find('div', id='main')
if main_div:
    panel_body = main_div.find('div', class_='panel-body')
    if panel_body:
        content_html = "".join(str(item) for item in panel_body.contents).strip()
        db_path = os.path.join(r'C:\Users\turga\OneDrive\Desktop\bürokratlar birliği site yedeği\burokratlarbirligi.org', 'instance', 'cms.db')
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("UPDATE page SET content_html=? WHERE slug='etkinlik'", (content_html,))
        conn.commit()
        conn.close()

print("Characters fixed in HTML and DB using explicit \ufffd replacements!")
