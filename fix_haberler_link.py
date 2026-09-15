import re
import os

files_to_update = ['anasayfa.html', 'hakkimizda.html']

for file in files_to_update:
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        # Replace haberler.html with haber-listesi.html
        content = content.replace('href="haberler.html"', 'href="haber-listesi.html"')
        
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"Updated {file}")

# Delete the dummy haberler.html
if os.path.exists('haberler.html'):
    os.remove('haberler.html')
    print("Deleted placeholder haberler.html")
