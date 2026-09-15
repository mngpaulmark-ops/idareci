import glob
import re

for file in glob.glob('*.html') + glob.glob('haber/*.html') + glob.glob('templates/*.html'):
    try:
        with open(file, 'r', encoding='utf-8') as f:
            page = f.read()
            
        new_page = page
        
        # Remove right:-80px from slideshoww
        new_page = new_page.replace('class="slideshoww" style="position:absolute; z-index:-99; right:-80px;"', 'class="slideshoww" style="position:absolute; z-index:-99;"')
        
        if new_page != page:
            with open(file, 'w', encoding='utf-8') as f:
                f.write(new_page)
    except Exception as e:
        pass

print("Header slideshow styling restored.")
