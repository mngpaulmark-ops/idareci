import glob

count_1 = 0
count_2 = 0

for f in glob.glob('**/*.html', recursive=True):
    try:
        with open(f, 'r', encoding='utf-8') as file:
            c = file.read()
        
        changed = False
        
        if '24.11.20220' in c:
            c = c.replace('24.11.20220', '24.11.2022')
            changed = True
            count_1 += 1
            
        if '23.02.20222' in c:
            c = c.replace('23.02.20222', '23.02.2022')
            changed = True
            count_2 += 1
            
        if changed:
            with open(f, 'w', encoding='utf-8') as file:
                file.write(c)
    except Exception as e:
        pass

print(f"Fixed 24.11.20220 in {count_1} files.")
print(f"Fixed 23.02.20222 in {count_2} files.")
