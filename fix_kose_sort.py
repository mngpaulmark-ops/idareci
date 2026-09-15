import glob
import os

count = 0
for filepath in glob.glob('*.py'):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'KoseYazisi.date_added.desc(), KoseYazisi.id.desc()' in content:
        print(f"Updating {filepath}")
        content = content.replace('KoseYazisi.date_added.desc(), KoseYazisi.id.desc()', 'KoseYazisi.date_added.desc(), KoseYazisi.date_added.desc(), KoseYazisi.id.desc()')
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        count += 1

print(f"Updated {count} files.")
