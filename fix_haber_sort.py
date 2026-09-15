import re

# Update update_anasayfa.py
with open('update_anasayfa.py', 'r', encoding='utf-8') as f:
    c = f.read()
c = c.replace('Haber.query.order_by(Haber.id.desc())', 'Haber.query.order_by(Haber.date.desc(), Haber.id.desc())')
with open('update_anasayfa.py', 'w', encoding='utf-8') as f:
    f.write(c)

# Update haber_helper.py
with open('haber_helper.py', 'r', encoding='utf-8') as f:
    c = f.read()
c = c.replace('Haber.query.order_by(Haber.id.desc())', 'Haber.query.order_by(Haber.date.desc(), Haber.id.desc())')
with open('haber_helper.py', 'w', encoding='utf-8') as f:
    f.write(c)

# Update app.py
with open('app.py', 'r', encoding='utf-8') as f:
    c = f.read()
c = c.replace('Haber.query.order_by(Haber.id.desc())', 'Haber.query.order_by(Haber.date.desc(), Haber.id.desc())')
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(c)

print("Updated sorting logic!")
