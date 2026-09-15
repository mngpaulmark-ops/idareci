import glob
import re
import bs4
from datetime import datetime

count_fixed = 0

for f in glob.glob('kose-yazar-*.html'):
    if f == 'kose-yazar-1-sayfa-60.html' or 'sayfa' in f:
        # ignore paginated for now, or process them too?
        pass

    try:
        with open(f, 'r', encoding='utf-8') as file:
            html = file.read()
            
        soup = bs4.BeautifulSoup(html, 'html.parser')
        
        # The list of articles is under <div class="col-md-8"> after "Yazarin Yazilari:"
        h4_tag = soup.find('h4', text=re.compile(r'Yazar.*?Yaz', re.IGNORECASE))
        if not h4_tag:
            h4_tag = soup.find('h4', string=re.compile(r'Yazar.*?Yaz', re.IGNORECASE))
            if not h4_tag:
                continue
                
        ul_tag = h4_tag.find_next_sibling('ul')
        if not ul_tag:
            continue
            
        li_tags = ul_tag.find_all('li')
        
        items = []
        for li in li_tags:
            a_tag = li.find('a')
            if not a_tag:
                continue
            text = a_tag.text
            
            # try to parse date
            m = re.search(r'(\d{1,2})[\.\-](\d{1,2})[\.\-](\d{4})', text)
            dt = datetime(1900, 1, 1) # default very old
            if m:
                try:
                    dt = datetime(int(m.group(3)), int(m.group(2)), int(m.group(1)))
                except:
                    pass
            
            # Extract ID from href for secondary sort
            href = a_tag.get('href', '')
            m_id = re.search(r'(\d+)\.html', href)
            yazi_id = int(m_id.group(1)) if m_id else 0
                    
            items.append((dt, yazi_id, li))
            
        if not items:
            continue
            
        # Sort items: date descending, then id descending
        items.sort(key=lambda x: (x[0], x[1]), reverse=True)
        
        # Clear ul and append sorted
        ul_tag.clear()
        for item in items:
            ul_tag.append(item[2])
            
        with open(f, 'w', encoding='utf-8') as file:
            file.write(str(soup))
            
        count_fixed += 1
            
    except Exception as e:
        print(f"Error on {f}: {e}")

print(f"Sorted articles in {count_fixed} kose-yazar-*.html files.")
