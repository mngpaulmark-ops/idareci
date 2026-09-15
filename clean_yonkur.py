import glob

for file in glob.glob('templates/admin/yonkur*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = content.replace('<option value="te">Temsilcilikler</option>', '')
    content = content.replace("{% elif m.grup == 'te' %}Temsilcilikler", '')
        
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
print('Removed Temsilcilik from Yonkur templates')
