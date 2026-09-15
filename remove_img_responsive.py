import re

with open('galeri_helper.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove img-responsive from the album list
content = content.replace('class="img-responsive rounded shadow"', 'class="rounded shadow"')

with open('galeri_helper.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Removed img-responsive from galeri_helper.py")
