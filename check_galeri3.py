import bs4
with open('galeri-resimler-1.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

soup = bs4.BeautifulSoup(text, 'lxml')
print(soup.title.string)
for img in soup.find_all('img')[:15]:
    print(img.get('src'))
