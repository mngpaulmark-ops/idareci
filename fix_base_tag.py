import glob
import re

print("Injecting <base href=\"/\"> into all HTML files...")

count = 0
for file in glob.glob('*.html') + glob.glob('haber/*.html') + glob.glob('sayfa/*.html'):
    with open(file, 'r', encoding='utf-8', errors='surrogateescape') as f:
        page = f.read()
    
    if '<base href="/">' not in page:
        # Insert right after <head>
        new_page = re.sub(r'(<head[^>]*>)', r'\1\n<base href="/">', page, count=1, flags=re.IGNORECASE)
        if new_page != page:
            with open(file, 'w', encoding='utf-8', errors='surrogateescape') as f:
                f.write(new_page)
            count += 1

print(f"Injected base tag into {count} files.")
