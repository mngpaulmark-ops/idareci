import glob
import os

count_base = 0

for f in glob.glob('**/*.html', recursive=True):
    try:
        with open(f, 'r', encoding='utf-8') as file:
            c = file.read()
        
        changed = False
        
        if '<base href="/idareci/" />' not in c:
            if '<head>' in c:
                c = c.replace('<head>', '<head>\n<base href="/idareci/" />')
                changed = True
                count_base += 1
            elif '</title>' in c:
                c = c.replace('</title>', '</title>\n<base href="/idareci/" />')
                changed = True
                count_base += 1
            elif '<HEAD>' in c:
                c = c.replace('<HEAD>', '<HEAD>\n<base href="/idareci/" />')
                changed = True
                count_base += 1
                
        if changed:
            with open(f, 'w', encoding='utf-8') as file:
                file.write(c)
    except Exception as e:
        print(f"Error on {f}: {e}")

print(f"Added base tag to {count_base} files.")
