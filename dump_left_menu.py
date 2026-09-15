import re
c=open('anasayfa.html', encoding='utf-8', errors='ignore').read()
match = re.search(r'<ul id="left-menu">', c)
if match:
    idx = match.start()
    print(c[max(0, idx-200):idx+500])
