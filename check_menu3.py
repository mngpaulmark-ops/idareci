import bs4
soup = bs4.BeautifulSoup(open('anasayfa.html', encoding='utf-8').read(), 'lxml')
p = soup.find(class_='left-menu')
while p and p.name != 'body':
    print(p.name, p.get('class'))
    p = p.parent
