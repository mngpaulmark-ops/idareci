import re

with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

pattern_model = r'(saat = db\.Column\(db\.String\(50\), nullable=True\))'
replacement_model = r'\1\n    location = db.Column(db.String(255), nullable=True)'

code = re.sub(pattern_model, replacement_model, code)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated Etkinlik model")
