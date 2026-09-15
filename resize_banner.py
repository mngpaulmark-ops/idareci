import re
import os

files_to_update = ['anasayfa.html', 'hakkimizda.html']

for file in files_to_update:
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        # The current style is: style="width: 100%; max-width: 250px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); border: 1px solid #eee;"
        # I want to change it to: style="width: 100%; height: 200px; object-fit: fill; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); border: 1px solid #eee;"
        # 200px is more than 2x of 81px.
        
        # We can just use a regex to replace the img tag
        pattern = r'<img src="data/yanaplat\.gif" alt="Milli İrade Platformu" style="[^"]*" />'
        replacement = '<img src="data/yanaplat.gif" alt="Milli İrade Platformu" style="width: 100%; height: 220px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); border: 1px solid #ccc;" />'
        
        new_content = re.sub(pattern, replacement, content)
        
        with open(file, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        print(f"Updated {file}")
