import os, glob

html_files = glob.glob('*.html')
count = 0
for file in html_files:
    try:
        with open(file, 'r', encoding='utf-8') as f:
            text = f.read()
        
        target = '/" target="_blank" title=""></a>'
        if target in text:
            new_text = text.replace(target, 'Biz Birlikte Güçlüyüz')
            with open(file, 'w', encoding='utf-8') as f:
                f.write(new_text)
            count += 1
    except Exception as e:
        pass
print(f'Replaced in {count} files.')
