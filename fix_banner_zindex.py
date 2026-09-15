import glob
import re

count = 0
for f in glob.glob('**/*.html', recursive=True):
    try:
        with open(f, 'r', encoding='utf-8', errors='ignore') as file:
            c = file.read()
            
        original_c = c
        
        # We want to change the z-index of the top banner
        c = c.replace('z-index: -90;', 'z-index: 1;')
        
        # We also want to make sure the logo is above the banner just in case
        # <img alt="İdareci ve Bürokratlar Birliği Derneği" class="logo img-responsive" src="data/9595428-logo.png" style="margin-top:15px;"/>
        
        c = re.sub(r'class="logo img-responsive" src="data/9595428-logo\.png" style="margin-top:15px;"', r'class="logo img-responsive" src="data/9595428-logo.png" style="margin-top:15px; position:relative; z-index:2;"', c)
        
        if c != original_c:
            with open(f, 'w', encoding='utf-8') as file:
                file.write(c)
            count += 1
            
    except Exception as e:
        pass

print(f"Fixed banner z-index in {count} files.")
