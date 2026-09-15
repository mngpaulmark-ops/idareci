import re
with open('anasayfa.html', 'r', encoding='utf-8') as f:
    text = f.read()

pattern = re.compile(r'(<ul[^>]*id="duyurular"[^>]*>).*?(</ul>)', re.DOTALL | re.IGNORECASE)
new_content = r'\1\n<li class="news-item"><a href="#">İdareci ve Bürokratlar Birliği Derneği Web Sitesine Hoşgeldiniz...</a></li>\n\2'
text = pattern.sub(new_content, text)

with open('anasayfa.html', 'w', encoding='utf-8') as f:
    f.write(text)
print('Updated anasayfa.html')
