import bs4

html = '<ul id="left-menu"><li>New</li></ul>'
new_bs = bs4.BeautifulSoup(html, 'html.parser')
print(repr(str(new_bs)))
