import re

with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

temsil_html = """
    # 4. Temsilcilik
    temsil_html = '<div class="main"><div class="panel panel-primary">'
    temsil_html += generate_group_html('Temsilcilikler', groups['te'])
    temsil_html += '</div></div>'
    write_to_file_and_db('temsilcilik.html', temsil_html, 'Temsilcilik')
"""

# The exact string is probably something like: write_to_file_and_db('yuksek-istisare-onur-kurulu-uyesi.html', istisare_html, 'Yksek stiare ve Onur Kurulu')
# We'll just regex replace before `@app.route('/admin/yonkur')`
if '# 4. Temsilcilik' not in code:
    code = code.replace("@app.route('/admin/yonkur')", temsil_html + "\n@app.route('/admin/yonkur')")
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(code)
    print("Updated regenerate_yonkur_html in app.py")
