import json
from app import db, app, Etkinlik, Page
import re
import os
import bs4

def parse_date(date_str):
    if not date_str:
        return (0, 0, 0)
    nums = re.findall(r'\d+', date_str)
    if len(nums) >= 3:
        return (int(nums[2]), int(nums[1]), int(nums[0]))
    return (0, 0, 0)

def regenerate_anasayfa_etkinlikler():
    with app.app_context():
        etkinlikler_db = Etkinlik.query.all()
        etkinlikler = sorted(etkinlikler_db, key=lambda x: parse_date(x.edate), reverse=True)
        
        events_list = []
        for e in etkinlikler:
            events_list.append({
                "date": getattr(e, 'edate', "") or "",
                "saat": getattr(e, 'saat', "") or "",
                "type": e.type or "meeting",
                "title": (e.title or "").replace('\\r', '').replace('\\n', ' '),
                "description": (e.description or "").replace('\\r', '').replace('\\n', ' '),
                "url": e.link or ""
            })
        
        # We also sanitize actual newline characters just to be safe
        for e in events_list:
            e["description"] = e["description"].replace('\r', '').replace('\n', ' ')
            e["title"] = e["title"].replace('\r', '').replace('\n', ' ')
            
        events_json = json.dumps(events_list, ensure_ascii=False, indent=4)
        
        for file in ['anasayfa.html', 'index.html']:
            try:
                if os.path.exists(file):
                    with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                        text = f.read()
                    pattern = r'var eventsInline = \[.*?\];'
                    
                    # Fix JS crash by passing a lambda instead of a string, so re.sub doesn't process escape sequences like \n
                    new_text = re.sub(pattern, lambda m: 'var eventsInline = ' + events_json + ';', text, flags=re.DOTALL)
                    
                    if new_text == text:
                        pattern2 = r'var eventsInline = .*?;'
                        new_text = re.sub(pattern2, lambda m: 'var eventsInline = ' + events_json + ';', text, flags=re.DOTALL)
                        
                    with open(file, 'w', encoding='utf-8') as f:
                        f.write(new_text)
            except Exception as e:
                print(f"Error updating {file} events:", e)

        html_blocks = []
        for e in etkinlikler:
            tarih = getattr(e, 'edate', "") or ""
            saat = getattr(e, 'saat', "") or ""
            yer = getattr(e, 'location', "") or ""
            
            block = f'''<h4>
    <a href="" target="_blank">
        <br/>
        Konu : {e.title}
    </a>
</h4>
<span>
    Açıklama :
    <span>
        {e.description}
    </span>
    <br/>
    Tarih :
    <b>
        {tarih}
    </b>
    Saat :
    <b>
        {saat}
    </b>
    <br/>
    Yer : {yer}
    <div class="col-md-12" style="border-bottom:1px solid  #CCC">
    </div>
</span>'''
            html_blocks.append(block)
            
        full_html = "".join(html_blocks)
        
        page = Page.query.filter_by(slug='etkinlik').first()
        if page:
            page.content_html = full_html
            db.session.commit()
            
        for filename in ['etkinlik.html', 'etkinlikler.html']:
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8', errors='surrogateescape') as f:
                    local_html = f.read()
                soup = bs4.BeautifulSoup(local_html, 'html.parser')
                main_div = soup.find('div', id='main')
                if main_div:
                    panel_body = main_div.find('div', class_='panel-body')
                    if panel_body:
                        panel_body.clear()
                        new_content_soup = bs4.BeautifulSoup(full_html, 'html.parser')
                        panel_body.append(new_content_soup)
                        with open(filename, 'w', encoding='utf-8', errors='surrogateescape') as f:
                            f.write(str(soup))

if __name__ == '__main__':
    regenerate_anasayfa_etkinlikler()
    print("Regenerated anasayfa.html and index.html etkinlikler JSON, and etkinlik.html HTML.")
