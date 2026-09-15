import os, glob
count = 0
for f in glob.glob('**/*.html', recursive=True):
    try:
        with open(f, 'r', encoding='utf-8') as file:
            c = file.read()
        if '<base href="/"' in c:
            c = c.replace('<base href="/"/>', '<base href="/idareci/"/>').replace('<base href="/" />', '<base href="/idareci/"/>')
            with open(f, 'w', encoding='utf-8') as file:
                file.write(c)
            count += 1
    except Exception as e:
        pass
print(f'Updated {count} files')
