import re
with open('galeri-resimler-1.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()
print('\n'.join(re.findall(r'<img [^>]*src=["\'](.*?)["\']', text)[:20]))
