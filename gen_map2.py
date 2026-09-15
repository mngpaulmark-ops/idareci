chars = 'ğĞıİşŞöÖüÜçÇ'
mapping = {}
for c in chars:
    try:
        mojibake = c.encode('utf-8').decode('cp1252')
        mapping[mojibake] = c
    except:
        pass
with open('mojibake_map.py', 'a', encoding='utf-8') as f:
    f.write('MOJIBAKE_MAP_1252 = ' + repr(mapping) + '\n')
