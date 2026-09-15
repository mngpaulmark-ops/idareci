import bs4

html = '<div><ul id="left-menu"><li>Old</li></ul></div>'
soup = bs4.BeautifulSoup(html, 'lxml')
old = soup.find('ul', id='left-menu')
new_html = '<ul id="left-menu"><li>New</li></ul>'
new_bs = bs4.BeautifulSoup(new_html, 'html.parser')
old.replace_with(new_bs)
print(str(soup))
