import re

with open('app.py', 'r', encoding='utf-8', errors='surrogateescape') as f:
    code = f.read()
    
# Add location to Etkinlik model
if 'location = db.Column(db.String(255), nullable=True)' not in code:
    code = code.replace("link = db.Column(db.String(255), default='')", "link = db.Column(db.String(255), default='')\n    location = db.Column(db.String(255), nullable=True)")

# Update admin_etkinlik_ekle
if 'location = request.form.get(\'location\')' not in code:
    code = code.replace("saat = request.form.get('saat')", "saat = request.form.get('saat')\n        location = request.form.get('location')")
    code = code.replace("yeni = Etkinlik(title=title, description=description, edate=edate, saat=saat)", "yeni = Etkinlik(title=title, description=description, edate=edate, saat=saat, location=location)")

# Update admin_etkinlik_edit
if 'etkinlik.location = request.form.get(\'location\')' not in code:
    code = code.replace("etkinlik.saat = request.form.get('saat')", "etkinlik.saat = request.form.get('saat')\n        etkinlik.location = request.form.get('location')")

with open('app.py', 'w', encoding='utf-8', errors='surrogateescape') as f:
    f.write(code)

print("Updated app.py Etkinlik model and routes with location.")
