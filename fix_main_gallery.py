import re

with open('galeri_helper.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the main albums to be 350px tall (they are currently 150px tall and col-md-6)
# The pattern for main albums in galeri_helper.py:
# <img src="{thumb_url}" class="rounded shadow" style="width:100%; height:150px !important; font-size:16px; object-fit:cover; border-radius:8px; border:2px solid #ccc;" onerror="this.src='themes/burokratlar/tema/images/no-image.png'"/>
content = content.replace(
    'style="width:100%; height:150px !important; font-size:16px;',
    'style="width:100%; height:350px !important; font-size:16px;'
)

with open('galeri_helper.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Restored main albums to 350px height.")
