import urllib.request
import bs4
import sqlite3
import os
import re

url = 'https://burokratlarbirligi.org/etkinlikler.html'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
resp = urllib.request.urlopen(req)
html = resp.read().decode('utf-8', errors='replace')

soup = bs4.BeautifulSoup(html, 'html.parser')
main_div = soup.find('div', id='main')

if main_div:
    panel_body = main_div.find('div', class_='panel-body')
    if panel_body:
        content_html = "".join(str(item) for item in panel_body.contents).strip()
        
        # Exact word replacements for known U+FFFD instances in the events text
        replacements = {
            '\ufffdUBAT': 'ŞUBAT',
            'YA\ufffdAYAN': 'YAŞAYAN',
            'B\ufffdR\ufffd': 'BİRİ',
            'GEN\ufffd': 'GENÇ',
            'BAKI\ufffd': 'BAKIŞ',
            'A\ufffdISIYLA': 'AÇISIYLA',
            'HAFTAK\ufffd': 'HAFTAKİ',
            'KONU\ufffdUMUZ': 'KONUĞUMUZ',
            'H\ufffdK\ufffdMET\ufffdN': 'HÜKÜMETİN',
            'PART\ufffd': 'PARTİ',
            'ET\ufffdK': 'ETİK',
            'BA\ufffdKANI': 'BAŞKANI',
            'CEM\ufffdL': 'CEMİL',
            'TUN\ufffd': 'TUNÇ',
            'M\ufffdLLET': 'MİLLET',
            'konu\ufffdu': 'konuğu',
            'Cumhurba\ufffdkan\ufffd': 'Cumhurbaşkanı',
            'Ba\ufffddan\ufffdman\ufffd': 'Başdanışmanı',
            'Say\ufffdn': 'Sayın',
            '\ufffderef': 'Şeref',
            'Malko\ufffd': 'Malkoç',
            'Kat\ufffdlacakt\ufffdr': 'Katılacaktır',
            'ABD\ufffdLHAM\ufffdD': 'ABDÜLHAMİD',
            'TAYY\ufffdP': 'TAYYİP',
            'ERDO\ufffdAN': 'ERDOĞAN',
            '\ufffdOK': 'ÇOK',
            'KONU\ufffdULACAK': 'KONUŞULACAK',
            'Medyas\ufffd': 'Medyası',
            '\ufffdle': 'İle',
            'M\ufffdcadelenin': 'Mücadelenin',
            'l\ufffd\ufffdten': 'lütfen',
            'l\ufffdten': 'lütfen',
            'propagandas\ufffd': 'propagandası',
            'ara\ufffdlar\ufffd': 'araçları',
            '\ufffdlkeleri': 'ülkeleri',
            'Ter\ufffdr': 'Terör',
            'G\ufffd\ufffd': 'Göç',
            '\ufffdMD\ufffdDEN': 'ŞİMDİDEN',
            'TAR\ufffdH\ufffd': 'TARİHİ',
            'SAAT\ufffd': 'SAATİ',
            'ger\ufffdek': 'gerçek',
            'y\ufffdz\ufffd': 'yüzü',
            '\ufffdrg\ufffdtleri': 'örgütleri',
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
            'DERNE\ufffd\ufffdND\ufffdE': 'DERNEĞİNDE',
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
            '\ufffddareci': 'İdareci',
            'B\ufffdr\ufffdokratlar': 'Bürokratlar',
            'Birli\ufffdi': 'Birliği',
            'Derne\ufffdi': 'Derneği',
            '\ufffd\ufffdlemler': 'İşlemler',
            'A\ufffdklama': 'Açıklama',
            'Tarih': 'Tarih',
            'Dokunulmazl\ufffdk': 'Dokunulmazlık',
            'dokunulmazl\ufffdklar\ufffdn': 'dokunulmazlıkların',
            'bilinmeyenler': 'bilinmeyenler'
        }
        
        # Also clean up any lingering U+FFFD around
        # The safer way is to replace specific known words first
        for k, v in replacements.items():
            content_html = content_html.replace(k, v)
        
        # Then just remove the rest of the generic \ufffd to avoid weird chars
        content_html = content_html.replace('\ufffd', '')
            
        content_html = content_html.replace("<span>", "<span>").replace("</span><br/>", "</span><br/>")
        
        # Save to DB
        db_path = os.path.join(r'C:\Users\turga\OneDrive\Desktop\bürokratlar birliği site yedeği\burokratlarbirligi.org', 'instance', 'cms.db')
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("UPDATE page SET content_html=? WHERE slug='etkinlik'", (content_html,))
        conn.commit()
        conn.close()
        
        for filename in ['etkinlik.html', 'etkinlikler.html']:
            path = os.path.join(r'C:\Users\turga\OneDrive\Desktop\bürokratlar birliği site yedeği\burokratlarbirligi.org', filename)
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8', errors='surrogateescape') as f:
                    local_html = f.read()
                    
                local_soup = bs4.BeautifulSoup(local_html, 'html.parser')
                local_main = local_soup.find('div', id='main')
                if local_main:
                    local_panel_body = local_main.find('div', class_='panel-body')
                    if local_panel_body:
                        local_panel_body.clear()
                        new_content_soup = bs4.BeautifulSoup(content_html, 'html.parser')
                        local_panel_body.append(new_content_soup)
                        
                        with open(path, 'w', encoding='utf-8', errors='surrogateescape') as f:
                            f.write(str(local_soup))
                        print(f"Updated {filename} correctly without breaking HTML!")

