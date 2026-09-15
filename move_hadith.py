import os
import glob
import re

for file in glob.glob('*.html') + glob.glob('haber/*.html') + glob.glob('templates/*.html'):
    if not os.path.isfile(file): continue
    try:
        with open(file, 'r', encoding='utf-8') as f:
            c = f.read()
    except: continue
    
    if 'hadis-i-serif' in c:
        # Extract the hadith widget block
        # It starts with <div class="panel panel-primary hadis-i-serif" and ends with </script>
        pattern = r'(<div class="panel panel-primary hadis-i-serif".*?</script>)\s*'
        match = re.search(pattern, c, flags=re.DOTALL)
        if match:
            hadith_html = match.group(1)
            # Remove it from its current place
            c = c.replace(match.group(0), '')
            
            # Now find the left-menu panel-primary and insert after it.
            # The menu ends with:
            # <li><a href="raporlar-belgeler.html" ...> Raporlar / Belgeler</a></li>
            # </ul>
            # </div>
            # </div>
            # (or something similar). We can just look for "Raporlar / Belgeler</a></li>\n\t\t\t\t\t\t</ul>\n\t\t\t\t\t</div>\n\t\t\t\t</div>"
            # Actually, looking for <!-- menu --> is safer, but does it exist?
            # Let's use a regex to find the end of the first panel-primary in left-menu.
            # A simpler way: Find '<div class="panel panel-kurumsal mb-4 side-dijital">' 
            # and inject it RIGHT BEFORE that!
            
            # Since side-dijital is immediately after the menu:
            if 'side-dijital' in c:
                c = re.sub(r'(<div[^>]*class="panel panel-kurumsal mb-4 side-dijital")', hadith_html + r'\n\n\1', c, count=1)
            else:
                # If side-dijital is not there, try finding the end of the ul inside panel-primary
                c = re.sub(r'(Raporlar / Belgeler.*?</ul>\s*</div>\s*</div>)', r'\1\n' + hadith_html + '\n', c, count=1, flags=re.DOTALL)
            
            with open(file, 'w', encoding='utf-8') as f:
                f.write(c)

print("Moved Hadith widget to right below the left menu!")
