import re

with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update Etkinlik Model
target_model = """    saat = db.Column(db.String(50), nullable=True)
    type = db.Column(db.String(50), default='meeting')"""

replacement_model = """    saat = db.Column(db.String(50), nullable=True)
    location = db.Column(db.String(255), nullable=True)
    type = db.Column(db.String(50), default='meeting')"""

code = code.replace(target_model, replacement_model)

# 2. Update admin_etkinlik_ekle route
target_add = """        edate = request.form.get('edate')
        saat = request.form.get('saat')
        
        yeni = Etkinlik(title=title, description=description, edate=edate, saat=saat)"""

replacement_add = """        edate = request.form.get('edate')
        saat = request.form.get('saat')
        location = request.form.get('location')
        
        yeni = Etkinlik(title=title, description=description, edate=edate, saat=saat, location=location)"""

code = code.replace(target_add, replacement_add)

# 3. Update admin_etkinlik_edit route
target_edit = """        etkinlik.description = request.form.get('description')
        etkinlik.edate = request.form.get('edate')
        etkinlik.saat = request.form.get('saat')
        db.session.commit()"""

replacement_edit = """        etkinlik.description = request.form.get('description')
        etkinlik.edate = request.form.get('edate')
        etkinlik.saat = request.form.get('saat')
        etkinlik.location = request.form.get('location')
        db.session.commit()"""

code = code.replace(target_edit, replacement_edit)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated app.py with Etkinlik location field!")
