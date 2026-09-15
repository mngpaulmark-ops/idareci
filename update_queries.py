import re

for filename in ['generate_kose.py', 'app_kose.py']:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            c = f.read()
        
        c = c.replace('ORDER BY id DESC', 'ORDER BY date_added DESC, id DESC')
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(c)
    except:
        pass
        
print("Updated queries.")
