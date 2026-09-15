import glob
count = 0
for f in glob.glob('**/*.html', recursive=True):
    try:
        with open(f, 'r', encoding='utf-8') as file:
            c = file.read()
        if '<base href="/idareci/"' in c:
            new_c = c.replace('<base href="/idareci/"/>', '').replace('<base href="/idareci/" />', '')
            with open(f, 'w', encoding='utf-8') as file:
                file.write(new_c)
            count += 1
    except:
        pass
print(f"Removed base tag from {count} files")
