import re

c=open('anasayfa.html', encoding='utf-8', errors='ignore').read()
pattern_left = r'<ul id="left-menu">.*?</ul>'
match = re.search(pattern_left, c, flags=re.DOTALL)
print("MATCH LEFT:", bool(match))
if match:
    new_c = re.sub(pattern_left, 'REPLACED_LEFT_MENU', c, flags=re.DOTALL)
    print("Replace successful!")
