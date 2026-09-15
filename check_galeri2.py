import bs4
with open('galeri-resimler-1.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

soup = bs4.BeautifulSoup(text, 'lxml')
main = soup.find('div', id='main')
if main:
    for a in main.find_all('a'):
        print('A:', a.get('href'))
    for img in main.find_all('img'):
        print('IMG:', img.get('src'))
