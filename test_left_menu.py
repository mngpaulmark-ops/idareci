import re
c=open('anasayfa.html', encoding='utf-8', errors='ignore').read()
match = re.search(r'<ul id="left-menu">.*?</ul>', c, flags=re.DOTALL)
print("MATCH:", bool(match))
if match:
    print(match.group(0)[:150])
