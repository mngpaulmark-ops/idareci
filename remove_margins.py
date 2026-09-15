import os, re

with open('anasayfa.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Remove margin-bottom from side-banner
c = re.sub(r'(class="side-banner"[^>]*?)margin-bottom:\s*20px;?', r'\1margin-bottom: 0px;', c)

# Remove margin-top from hadis-i-serif
c = re.sub(r'(class="panel panel-primary hadis-i-serif"[^>]*?)margin-top:\s*20px;?', r'\1margin-top: 0px;', c)

with open('anasayfa.html', 'w', encoding='utf-8') as f:
    f.write(c)
