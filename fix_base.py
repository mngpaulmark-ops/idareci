import bs4
filepath = 'anasayfa.html'
soup = bs4.BeautifulSoup(open(filepath, encoding='utf-8').read(), 'lxml')
for b in soup.find_all('base'):
    b.decompose()
open(filepath, 'w', encoding='utf-8').write(str(soup))
