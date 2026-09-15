import sqlite3
import os
import bs4
import shutil

conn = sqlite3.connect('instance/cms.db')
c = conn.cursor()

c.execute('SELECT slug, title, content_html FROM page')
pages = c.fetchall()

# Use hakkimizda.html as the base template for any missing file
base_template_file = 'hakkimizda.html'
with open(base_template_file, 'r', encoding='utf-8', errors='surrogateescape') as f:
    base_html = f.read()

for slug, title, content in pages:
    filename = f"{slug}.html"
    if not os.path.exists(filename):
        # Create it from base template
        print(f"Creating missing file {filename} from base template.")
        html = base_html
    else:
        with open(filename, 'r', encoding='utf-8', errors='surrogateescape') as f:
            html = f.read()
    
    soup = bs4.BeautifulSoup(html, 'html.parser')
    main_div = soup.find('div', id='main')
    
    if main_div:
        # Update the title heading if exists
        heading = main_div.find('div', class_='panel-heading')
        if heading and '/' in heading.text:
            heading.string = f"İdareci ve Bürokratlar Birliği Derneği / {title}"
        elif heading:
            heading.string = title

        # Update the content
        panel_body = main_div.find('div', class_='panel-body')
        if panel_body:
            box = panel_body.find('div', class_='box')
            if box:
                box.clear()
                box.append(bs4.BeautifulSoup(content, 'html.parser'))
            else:
                panel_body.clear()
                panel_body.append(bs4.BeautifulSoup(content, 'html.parser'))
                
    # Update <title> tag
    title_tag = soup.find('title')
    if title_tag:
        title_tag.string = f"{title} | İdareci ve Bürokratlar Birliği Derneği"
        
    with open(filename, 'w', encoding='utf-8', errors='surrogateescape') as f:
        f.write(str(soup))
    print(f"Applied DB content to {filename}")

conn.close()
