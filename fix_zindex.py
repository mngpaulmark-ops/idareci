import re
import glob

files = glob.glob('*.html') + glob.glob('haber/*.html') + glob.glob('kose-yazilari*.html') + glob.glob('templates/*.html')

for file in files:
    try:
        with open(file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        new_content = content.replace('z-index:-99;', 'z-index: 1;')
        new_content = new_content.replace('z-index: -99;', 'z-index: 1;')
        
        if new_content != content:
            with open(file, 'w', encoding='utf-8') as f:
                f.write(new_content)
    except Exception as e:
        print(f"Error on {file}: {e}")

print("Updated z-index for slideshoww in all files.")
