import re

with open('anasayfa.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# The widgets are inside a <div class="row" style=" display: flex; flex-wrap: wrap;">
# Let's find it using bs4 to safely remove the entire row
import bs4
soup = bs4.BeautifulSoup(content, 'html.parser')
kamu = soup.find(id='panel-kamu-etigi')
if kamu:
    row = kamu.find_parent('div', class_='row')
    if row:
        row.decompose()
        
        with open('anasayfa.html', 'w', encoding='utf-8') as f:
            f.write(str(soup))
        print("Successfully removed the entire widget row from anasayfa.html")
    else:
        print("Could not find parent row.")
else:
    print("Could not find panel-kamu-etigi.")
