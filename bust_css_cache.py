import glob
import re

count = 0
for f in glob.glob('**/*.html', recursive=True):
    try:
        with open(f, 'r', encoding='utf-8', errors='ignore') as file:
            c = file.read()
            
        original_c = c
        
        # Bust style.css cache
        c = re.sub(r'style\.css(\?v=\d+)?', 'style.css?v=12', c)
        
        # Also explicitly add the responsive style directly into update_map.py's output (temsilcilik.html)
        # to ensure it's not relying solely on style.css just in case.
        
        if c != original_c:
            with open(f, 'w', encoding='utf-8') as file:
                file.write(c)
            count += 1
            
    except Exception as e:
        pass

print(f"Busted CSS cache in {count} files.")
