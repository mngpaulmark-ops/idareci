import glob
import re

bad_style_pattern = r'\.slideshoww\s*\{\s*max-width:50%.*?height:\s*155px\s*!important;\s*\}'
good_style = '''.slideshoww { max-width:100%; left:0px;  margin:0 auto; top:-1px; background-color:#FFF; }
.slideshoww img {position: absolute; top: 0px; left: 0px; z-index:-999; max-width:100%; background-color: #eee; }'''

for file in glob.glob('*.html') + glob.glob('haber/*.html') + glob.glob('templates/*.html'):
    try:
        with open(file, 'r', encoding='utf-8') as f:
            page = f.read()
            
        # Replace the bad style
        new_page = re.sub(bad_style_pattern, good_style, page, flags=re.DOTALL)
        
        if new_page != page:
            with open(file, 'w', encoding='utf-8') as f:
                f.write(new_page)
    except Exception as e:
        pass

print("Styles restored.")
