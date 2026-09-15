import bs4
import re

with open('anasayfa.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# Remove the old script that syncs TRT to leftPanel
text = re.sub(r'<script>\s*document\.addEventListener\("DOMContentLoaded", function\(\) {\s*setTimeout\(function\(\) {\s*var leftPanel = document\.querySelector[^\<]*</script>', '', text, flags=re.DOTALL)

soup = bs4.BeautifulSoup(text, 'lxml')

# Find the Haberler list-group
news_panel = soup.find('div', class_='news')
if news_panel:
    col6 = news_panel.find('div', class_='col-md-6')
    if col6:
        list_group = col6.find('div', class_='list-group')
        if list_group:
            # Set fixed height and scroll
            list_group['style'] = "height: 332px; overflow-y: auto; overflow-x: hidden; padding-right: 5px;"

# Make sure TRT widget doesn't have the inline height overwritten by JS? We removed the JS.
# TRT widget already has height: 332px inline from our earlier patch.

with open('anasayfa.html', 'w', encoding='utf-8') as f:
    f.write(str(soup))
    
print("Patched anasayfa.html")
