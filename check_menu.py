import bs4
soup = bs4.BeautifulSoup(open('anasayfa.html', encoding='utf-8').read(), 'lxml')
for tag in soup.find_all(True):
    if tag.string and 'Derneğimiz' in tag.string:
        print("Found in", tag.name)
        p = tag
        for i in range(5):
            p = p.parent
            print(f"Parent {i+1}: {p.name} class={p.get('class')}")
        break
