import re

c=open('anasayfa.html', encoding='utf-8', errors='ignore').read()
pattern_left = r'(<div class="panel-heading">\s*<img alt="Menu" src="themes/burokratlar/tema/images/icon-menu.png"/> Derneğimiz\s*</div>\s*<div class="panel-body">\s*)<ul id="left-menu">.*?</ul>(\s*</div>)'

match = re.search(pattern_left, c, flags=re.DOTALL)
print("MATCH FOUND:", bool(match))
