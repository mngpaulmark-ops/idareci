import glob

for file in glob.glob('*_helper.py') + ['app.py']:
    with open(file, 'r', encoding='utf-8') as f:
        c = f.read()
    
    if 'lxml' in c:
        c = c.replace("'lxml'", "'html.parser'")
        with open(file, 'w', encoding='utf-8') as f:
            f.write(c)
