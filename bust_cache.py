import glob, os, re
count = 0
for f in glob.glob('*.html') + glob.glob('haber/*.html'):
    if os.path.isfile(f):
        c = open(f, encoding='utf-8', errors='ignore').read()
        c = re.sub(r'css/style\.css(\?v=\d+)?', 'css/style.css?v=6', c)
        open(f, 'w', encoding='utf-8').write(c)
        count += 1
print('Cache busted in', count)
