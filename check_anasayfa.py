import re
with open('anasayfa.html', 'r', encoding='utf-8') as f:
    text = f.read()

match = re.search(r'<ul id="left-menu">.*?</ul>', text, re.DOTALL)
if match:
    print(repr(match.group(0)))
else:
    print('Not found')
