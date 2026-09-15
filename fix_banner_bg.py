import re
import os

files_to_update = ['anasayfa.html', 'hakkimizda.html']

for file in files_to_update:
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        # The current style is: style="width: 100%; height: 220px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); border: 1px solid #ccc;"
        # Let's fix the "kesik renk" by ensuring the background is white, using object-fit: contain, so the image isn't distorted or leaving cut-off background colors.
        # Wait, if they wanted it to stretch, object-fit: fill is default.
        # What if the background of the div is grey?
        # Let's wrap the img in a nice white card that fills the space.
        
        pattern = r'<img src="data/yanaplat\.gif" alt="Milli İrade Platformu" style="width: 100%; height: 220px; border-radius: 8px; box-shadow: 0 4px 8px rgba\(0,0,0,0\.1\); border: 1px solid #ccc;" />'
        
        # New style: white background for the banner, contain the image, no cuts.
        replacement = '<img src="data/yanaplat.gif" alt="Milli İrade Platformu" style="width: 100%; height: 220px; object-fit: contain; background-color: #ffffff; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); border: 1px solid #ccc; padding: 10px;" />'
        
        new_content = re.sub(pattern, replacement, content)
        
        with open(file, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        print(f"Updated {file}")
