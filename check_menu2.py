import bs4
soup = bs4.BeautifulSoup(open('anasayfa.html', encoding='utf-8').read(), 'lxml')
img = soup.find('img', alt='Menu')
p = img
for i in range(5):
    p = p.parent
    print(p.name, p.get('class'))
