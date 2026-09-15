import os
with open('galeri_helper.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('src="{img_path}"', 'src="{img_path.replace(\'data/gallery/\', \'data/gallery/thumb_\')}"')

with open('galeri_helper.py', 'w', encoding='utf-8') as f:
    f.write(text)

os.system('python galeri_helper.py')
