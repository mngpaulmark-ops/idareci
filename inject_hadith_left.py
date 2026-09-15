import os
import glob
import re

with open('inject_hadith_final2.py', encoding='utf-8') as f:
    hadith_html = f.read().split('hadith_html = """\n')[1].split('"""')[0]

files = glob.glob('*.html') + glob.glob('haber/*.html') + glob.glob('templates/*.html')
count = 0

for file in files:
    if os.path.isfile(file):
        try:
            with open(file, 'r', encoding='utf-8') as f:
                c = f.read()
        except:
            continue
            
        if 'daily-hadith' not in c:
            # First remove it if it's placed weirdly somewhere else (like before basin)
            c = c.replace(hadith_html + '\n<div class="basin">', '<div class="basin">')
            
            # Now find the end of left-menu and inject it there
            # <div class="left-menu"> ... </div>
            # We can use regex to find the closing div of left-menu.
            # But the easiest way is to find '<div class="side-banner"' which is the last item in left-menu!
            # Then find its closing </div>
            
            pattern = r'(<div class="side-banner".*?</div>\s*)'
            if re.search(pattern, c, flags=re.DOTALL):
                c = re.sub(pattern, r'\1' + hadith_html + '\n', c, count=1, flags=re.DOTALL)
                with open(file, 'w', encoding='utf-8') as f:
                    f.write(c)
                count += 1
            else:
                # Fallback: just put it before the closing </div> of left-menu
                # This is risky, let's just replace '<!-- menu -->' block end
                pass

print(f"Injected Hadith widget into {count} HTML files!")
