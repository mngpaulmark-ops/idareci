import re

with open('app.py', 'r', encoding='utf-8') as f:
    c = f.read()

old_add = """        h = Haber(title=title, content=content, slug=slug)
        file = request.files.get('image')"""

new_add = """        date_str = request.form.get('date')
        h = Haber(title=title, content=content, slug=slug)
        if date_str:
            import datetime
            try:
                h.date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
            except:
                pass
        file = request.files.get('image')"""

if old_add in c:
    c = c.replace(old_add, new_add)
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(c)
    print("Fixed admin_haber_add.")
else:
    print("Could not find block to replace.")
