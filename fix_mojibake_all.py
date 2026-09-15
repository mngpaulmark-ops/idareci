import os
import glob

replacements = {
    'Ã¼': 'ü', 'Ã¶': 'ö', 'Ã§': 'ç', 'ÄŸ': 'ğ', 'Ä±': 'ı', 'ÅŸ': 'ş',
    'Ãœ': 'Ü', 'Ã–': 'Ö', 'Ã‡': 'Ç', 'Äž': 'Ğ', 'Ä°': 'İ', 'Åž': 'Ş'
}

count = 0
for file in glob.glob('*.html') + glob.glob('haber/*.html') + glob.glob('koseyazisi/**/*.html', recursive=True):
    try:
        with open(file, 'r', encoding='utf-8', errors='ignore') as f:
            c = f.read()
            
        changed = False
        for bad, good in replacements.items():
            if bad in c:
                c = c.replace(bad, good)
                changed = True
                
        if changed:
            with open(file, 'w', encoding='utf-8') as f:
                f.write(c)
            count += 1
    except:
        pass

print(f"Fixed mojibake in {count} files.")
