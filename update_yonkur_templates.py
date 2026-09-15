import glob

for file in glob.glob('templates/admin/yonkur*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # yonkur_list
    if "{% elif m.grup == 'is' %}" in content:
        content = content.replace("{% elif m.grup == 'is' %}Yüksek İstişare ve Onur Kurulu", 
                                  "{% elif m.grup == 'is' %}Yüksek İstişare ve Onur Kurulu\n                    {% elif m.grup == 'te' %}Temsilcilikler")
        content = content.replace("{% elif m.grup == 'is' %}Yksek stiare ve Onur Kurulu", 
                                  "{% elif m.grup == 'is' %}Yksek stiare ve Onur Kurulu\n                    {% elif m.grup == 'te' %}Temsilcilikler")
        # cp1254 encoded possibly
        content = content.replace("{% elif m.grup == 'is' %}Yksek stiare ve Onur Kurulu", 
                                  "{% elif m.grup == 'is' %}Yüksek İstişare ve Onur Kurulu\n                    {% elif m.grup == 'te' %}Temsilcilikler")
    
    # yonkur_add / yonkur_edit
    if 'value="is"' in content and 'value="te"' not in content:
        content = content.replace('<option value="is">Yüksek İstişare ve Onur Kurulu</option>',
                                  '<option value="is">Yüksek İstişare ve Onur Kurulu</option>\n                            <option value="te">Temsilcilikler</option>')
        content = content.replace('<option value="is">Yksek stiare ve Onur Kurulu</option>',
                                  '<option value="is">Yüksek İstişare ve Onur Kurulu</option>\n                            <option value="te">Temsilcilikler</option>')
                                  
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
print('Updated templates for Temsilcilikler')
