import glob
import re

count_cleaned = 0

for f in glob.glob('**/*.html', recursive=True):
    try:
        with open(f, 'r', encoding='utf-8') as file:
            c = file.read()
            
        original_c = c
            
        # Remove all existing base tags (whether they are <base href="/"> or <base href="/idareci/" /> or commented ones)
        # We will match anything like <base href=...>
        # Or <!-- Removed by WebCopy --><!--<base href="/">--><!-- Removed by WebCopy -->
        
        c = re.sub(r'<!-- Removed by WebCopy --><!--<base href="[^"]+">--><!-- Removed by WebCopy -->', '', c)
        c = re.sub(r'<base href="[^"]+"\s*/?>', '', c)
        
        # Now there are NO base tags left in the document.
        # Let's inject exactly ONE right after <head> or <HEAD>
        
        if '<head>' in c:
            c = c.replace('<head>', '<head>\n<base href="/idareci/" />')
        elif '<HEAD>' in c:
            c = c.replace('<HEAD>', '<HEAD>\n<base href="/idareci/" />')
        elif '</title>' in c:
            c = c.replace('</title>', '</title>\n<base href="/idareci/" />')
            
        if c != original_c:
            with open(f, 'w', encoding='utf-8') as file:
                file.write(c)
            count_cleaned += 1
            
    except Exception as e:
        pass

print(f"Cleaned and fixed base tags in {count_cleaned} files.")
