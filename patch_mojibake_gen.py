with open('app.py', 'r', encoding='utf-8') as f:
    c = f.read()

# Replace the save part of regenerate_temsilcilik_html
old_save = """            with open(file, 'w', encoding='utf-8', errors='surrogateescape') as f:

                f.write(str(soup))"""
new_save = """            html_str = str(soup)
            replacements = {
                'Ã¼': 'ü', 'Ã¶': 'ö', 'Ã§': 'ç', 'ÄŸ': 'ğ', 'Ä±': 'ı', 'ÅŸ': 'ş',
                'Ãœ': 'Ü', 'Ã–': 'Ö', 'Ã‡': 'Ç', 'Äž': 'Ğ', 'Ä°': 'İ', 'Åž': 'Ş'
            }
            for bad, good in replacements.items(): html_str = html_str.replace(bad, good)
            with open(file, 'w', encoding='utf-8', errors='surrogateescape') as f:
                f.write(html_str)"""

if old_save in c:
    c = c.replace(old_save, new_save)
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(c)
    print("Patched regenerate_temsilcilik_html to prevent future mojibake")
else:
    print("Could not find the save block.")
