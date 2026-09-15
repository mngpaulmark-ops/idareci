import os, glob, re

html_files = glob.glob('*.html')
count = 0
for file in html_files:
    try:
        with open(file, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
        
        # We look for something like /" target="_blank" title=""...
        # and replace the whole thing inside that <div class="pull-right"> with 'Biz Birlikte Güçlüyüz'
        
        new_text = re.sub(
            r'<div class="pull-right">\s*/" target="_blank" title="".*?</div>', 
            '<div class="pull-right">\n\t\t\t\t\t\t\t\tBiz Birlikte Güçlüyüz\n</div>', 
            text, 
            flags=re.DOTALL
        )
        
        if new_text != text:
            with open(file, 'w', encoding='utf-8') as f:
                f.write(new_text)
            count += 1
    except Exception as e:
        print("Error on", file, e)
print(f'Replaced in {count} files using regex.')
