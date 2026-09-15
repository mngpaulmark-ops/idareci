import os

def fix_mojibake(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
        
    replacements = {
        'Ã¼': 'ü', 'Ã¶': 'ö', 'Ã§': 'ç', 'ÄŸ': 'ğ', 'Ä±': 'ı', 'ÅŸ': 'ş',
        'Ãœ': 'Ü', 'Ã–': 'Ö', 'Ã‡': 'Ç', 'Äž': 'Ğ', 'Ä°': 'İ', 'Åž': 'Ş'
    }
    
    changed = False
    for bad, good in replacements.items():
        if bad in c:
            c = c.replace(bad, good)
            changed = True
            
    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f"Fixed {filepath}")
    else:
        print(f"No mojibake found in {filepath}")

fix_mojibake('temsilcilik.html')
