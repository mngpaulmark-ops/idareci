import re
with open('live_page.html', encoding='utf-8', errors='ignore') as f:
    html = f.read()
links = set(re.findall(r'href=[\'"](http[^\'"]+)[\'"]', html))
for l in links:
    if 'burokratlar' not in l:
        print(l)
