import re

with open('app.py', 'r', encoding='utf-8') as f:
    c = f.read()

# Fix Menu
c = re.sub(
    r'class Menu\(db\.Model\):\s*id = db\.Column\(db\.Integer, primary_key=True\)\s*title = db\.Column\(db\.String\(100\), nullable=False\)\s*date = db\.Column\(db\.String\(50\)\)\s*location = db\.Column\(db\.String\(100\)\)',
    r'class Menu(db.Model):\n    id = db.Column(db.Integer, primary_key=True)\n    title = db.Column(db.String(100), nullable=False)',
    c, count=1
)

# Fix LeftMenu
c = re.sub(
    r'class LeftMenu\(db\.Model\):\s*id = db\.Column\(db\.Integer, primary_key=True\)\s*title = db\.Column\(db\.String\(100\), nullable=False\)\s*date = db\.Column\(db\.String\(50\)\)\s*location = db\.Column\(db\.String\(100\)\)',
    r'class LeftMenu(db.Model):\n    id = db.Column(db.Integer, primary_key=True)\n    title = db.Column(db.String(100), nullable=False)',
    c, count=1
)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(c)

print("Fixed models.")
