import os, glob
for f in glob.glob('templates/**/*.html', recursive=True):
    with open(f, 'r', encoding='utf-8', errors='ignore') as file:
        c = file.read()
    c = c.replace('<base href="/idareci/" />', '')
    with open(f, 'w', encoding='utf-8') as file:
        file.write(c)
print("Removed base href from templates.")
