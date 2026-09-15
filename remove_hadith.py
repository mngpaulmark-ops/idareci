import os
with open('inject_hadith_final2.py', encoding='utf-8') as f:
    hadith_html = f.read().split('hadith_html = """\n')[1].split('"""')[0]

with open('anasayfa.html', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace(hadith_html + '\n<div class="basin">', '<div class="basin">')

with open('anasayfa.html', 'w', encoding='utf-8') as f:
    f.write(c)
