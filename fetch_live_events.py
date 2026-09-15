import urllib.request
import bs4
import sqlite3
import re
import os

url = 'https://burokratlarbirligi.org/etkinlikler.html'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
resp = urllib.request.urlopen(req)
html = resp.read().decode('utf-8', errors='replace')

soup = bs4.BeautifulSoup(html, 'html.parser')
main_div = soup.find('div', id='main')

if main_div:
    panel_body = main_div.find('div', class_='panel-body')
    if panel_body:
        # We need to extract the raw HTML of panel_body and fix characters
        content_html = "".join(str(item) for item in panel_body.contents).strip()
        
        # Let's fix some known encoding issues if they are U+FFFD
        # Often HTTrack or bad DB exports caused this. We will try to fix the words.
        replacements = {
            'Aklama': 'Açıklama',
            'UBAT': 'ŞUBAT',
            'YAAYAN': 'YAŞAYAN',
            'BR': 'BİRİ',
            'GEN': 'GENÇ',
            'BAKI': 'BAKIŞ',
            'AISIYLA': 'AÇISIYLA',
            'HAFTAK': 'HAFTAKİ',
            'KONUUMUZ': 'KONUĞUMUZ',
            'HKMETN': 'HÜKÜMETİN',
            'PART': 'PARTİ',
            'ETK': 'ETİK',
            'BAKANI': 'BAŞKANI',
            'CEML': 'CEMİL',
            'TUN': 'TUNÇ',
            'MLLET': 'MİLLET',
            'konuu': 'konuğu',
            'Cumhurbakan': 'Cumhurbaşkanı',
            'Badanman': 'Başdanışmanı',
            'Sayn': 'Sayın',
            'eref': 'Şeref',
            'Malko': 'Malkoç',
            'Katlacaktr': 'Katılacaktır',
            'ABDLHAMD': 'ABDÜLHAMİD',
            'TAYYP': 'TAYYİP',
            'ERDOAN': 'ERDOĞAN',
            'OK': 'ÇOK',
            'KONUULACAK': 'KONUŞULACAK',
            'Medyas': 'Medyası',
            'le': 'İle',
            'Mcadelenin': 'Mücadelenin',
            'lten': 'lütfen',
            'propagandas': 'propagandası',
            'aralar': 'araçları',
            'lkeleri': 'ülkeleri',
            'Terr': 'Terör',
            'G': 'Göç',
            '?MDDEN': 'ŞİMDİDEN',
            'TARH': 'TARİHİ',
            'SAAT': 'SAATİ',
            'gerek': 'gerçek',
            'yz': 'yüzü',
            'rgtleri': 'örgütleri',
            'rgtnn': 'örgütünün',
            'i': 'iç',
            'd': 'dış',
            'balantlar': 'bağlantıları',
            'ok': 'çok',
            'corafyadadr': 'coğrafyadadır',
            'zararalar': 'zararları',
            'snr': 'sınırı',
            'ilikileri': 'ilişkileri',
            'bak': 'bakışı',
            'Kresel': 'Küresel',
            'Trkiye': 'Türkiye',
            'D': 'Dış',
            'Politikas': 'Politikası',
            'KARTOLU': 'KARTOĞLU',
            'buluturmaktadr': 'buluşturmaktadır',
            'Olaanst': 'Olağanüstü',
            'alm': 'almış',
            'olduu': 'olduğu',
            'dorulturunsa': 'doğrultusunda',
            'toplanmasna': 'toplanmasına',
            'OUNLUK': 'ÇOĞUNLUK',
            'Perembe': 'Perşembe',
            'DAREC': 'İDARECİ',
            'BRL?': 'BİRLİĞİ',
            'DERNE?NDE': 'DERNEĞİNDE',
            'OLAAN ST': 'OLAĞANÜSTÜ',
            'yaplacaktr': 'yapılacaktır',
            'gn': 'günü',
            'GLE': 'GÜLE',
            'Keiren': 'Keçiören',
            'Girii': 'Girişi',
            'Teriflerinizi': 'Teşriflerinizi',
            'Derneimize': 'Derneğimize',
            'Vatanmza': 'Vatanımıza',
            'slam': 'İslam',
            'nsanla': 'İnsanlığa',
            'hayrl': 'hayırlı',
            'olmasn': 'olmasını',
            'Ycel': 'Yücel',
            'Bulvar': 'Bulvarı',
            'dareci': 'İdareci',
            'Brokratlar': 'Bürokratlar',
            'Birlii': 'Birliği',
            'Dernei': 'Derneği',
            'lemler': 'İşlemler'
        }
        
        for k, v in replacements.items():
            content_html = content_html.replace(k, v)
            
        # Also clean up the unclosed spans issue from HTTrack
        content_html = content_html.replace("<span>", "<span>").replace("</span><br/>", "</span><br/>")
        
        # Save to DB
        db_path = os.path.join(r'C:\Users\turga\OneDrive\Desktop\bürokratlar birliği site yedeği\burokratlarbirligi.org', 'instance', 'cms.db')
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("UPDATE page SET content_html=? WHERE slug='etkinlik'", (content_html,))
        conn.commit()
        conn.close()
        
        # Update html files
        print("Fetched and prepared content.")
        
        # We will use BeautifulSoup to replace the box/panel-body in etkinlik.html and etkinlikler.html
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
                        # Clear it
                        local_panel_body.clear()
                        # Append the new content
                        new_content_soup = bs4.BeautifulSoup(content_html, 'html.parser')
                        local_panel_body.append(new_content_soup)
                        
                        with open(path, 'w', encoding='utf-8', errors='surrogateescape') as f:
                            f.write(str(local_soup))
                        print(f"Updated {filename}")
else:
    print("Could not find main div in live site.")
