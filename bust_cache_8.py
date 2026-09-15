import glob, os, re
count = 0
for f in glob.glob('*.html') + glob.glob('haber/*.html'):
    if os.path.isfile(f):
        try:
            c = open(f, encoding='utf-8').read()
        except:
            continue
        c = re.sub(r'css/style\.css(\?v=\d+)?', 'css/style.css?v=8', c)
        open(f, 'w', encoding='utf-8').write(c)
        count += 1
print('Cache busted in', count)
