import sqlite3
import urllib.request
import bs4
import re

conn = sqlite3.connect('instance/cms.db')
c = conn.cursor()

c.execute('SELECT id, slug, title FROM page')
pages = c.fetchall()

for p_id, slug, title in pages:
    url = f"https://burokratlarbirligi.org/{slug}.html"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')
        soup = bs4.BeautifulSoup(html, 'html.parser')
        
        # In the original theme, page content is usually inside <div class="box"> inside <div class="panel-body">
        # Let's find the main content panel
        main_div = soup.find('div', id='main')
        if main_div:
            box = main_div.find('div', class_='box')
            if box:
                # We extract the inner HTML of the box
                content_html = "".join(str(item) for item in box.contents).strip()
                
                # Clean up any weird encodings if necessary (though beautifulsoup + utf-8 usually handles it)
                # Now update the database!
                c.execute('UPDATE page SET content_html=? WHERE id=?', (content_html, p_id))
                print(f"Updated '{slug}' from live website!")
            else:
                print(f"Box not found for '{slug}'")
        else:
            print(f"Main div not found for '{slug}'")
            
    except Exception as e:
        print(f"Error fetching '{slug}': {e}")

conn.commit()
conn.close()
print("All pages synced from live site!")
