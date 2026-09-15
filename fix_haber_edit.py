import re

with open('app.py', 'r', encoding='utf-8') as f:
    c = f.read()

old_edit = """        h.title = request.form.get('title')
        h.content = request.form.get('content')
        h.slug = request.form.get('slug')"""

new_edit = """        h.title = request.form.get('title')
        h.content = request.form.get('content')
        slug = request.form.get('slug')
        if slug:
            h.slug = slug
        date_str = request.form.get('date')
        if date_str:
            import datetime
            try:
                h.date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
            except:
                pass"""

if old_edit in c:
    c = c.replace(old_edit, new_edit)
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(c)
    print("Fixed admin_haber_edit.")
else:
    print("Could not find block to replace.")
