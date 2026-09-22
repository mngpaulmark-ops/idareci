import re

with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Fix 1: adding location to Etkinlik creation
pattern_add = r'yeni = Etkinlik\(title=title, description=description, edate=edate, saat=saat\)'
replacement_add = r"location = request.form.get('location')\n        yeni = Etkinlik(title=title, description=description, edate=edate, saat=saat, location=location)"

code = re.sub(pattern_add, replacement_add, code)

# Fix 2: adding location to Etkinlik edit
pattern_edit = r'etkinlik\.saat = request\.form\.get\(\'saat\'\)\s*db\.session\.commit\(\)'
replacement_edit = r"etkinlik.saat = request.form.get('saat')\n        etkinlik.location = request.form.get('location')\n        db.session.commit()"

code = re.sub(pattern_edit, replacement_edit, code)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated app.py with correct location handling")
