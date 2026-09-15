import glob, re
import os

count_base = 0
count_dots = 0

for f in glob.glob('**/*.html', recursive=True):
    try:
        with open(f, 'r', encoding='utf-8') as file:
            c = file.read()
        
        changed = False
        
        # 1. Re-add base tag if missing
        if '<base href' not in c:
            if '<head>' in c:
                c = c.replace('<head>', '<head>\n<base href="/idareci/" />')
                changed = True
                count_base += 1
            elif '</title>' in c:
                c = c.replace('</title>', '</title>\n<base href="/idareci/" />')
                changed = True
                count_base += 1
        
        # 2. Remove all ../ or ../../ from src and href
        # Because we have base tag, everything should just be relative to root of repo (e.g. data/... or themes/...)
        new_c = re.sub(r'(src|href)="\.\./\.\./', r'\1="', c)
        new_c = re.sub(r'(src|href)="\.\./', r'\1="', new_c)
        
        if new_c != c:
            c = new_c
            changed = True
            count_dots += 1
            
        if changed:
            with open(f, 'w', encoding='utf-8') as file:
                file.write(c)
    except Exception as e:
        print(f"Error on {f}: {e}")

print(f"Added base tag to {count_base} files.")
print(f"Removed ../ from {count_dots} files.")
