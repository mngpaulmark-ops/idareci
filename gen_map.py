chars = 'ğĞıİşŞöÖüÜçÇ'
mapping = {}
for c in chars:
    try:
        mojibake = c.encode('utf-8').decode('cp1250')
        mapping[mojibake] = c
    except:
        pass

with open('mojibake_map.py', 'w', encoding='utf-8') as f:
    f.write(f'MOJIBAKE_MAP = {repr(mapping)}\n')
