with open('app.py', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace('CITIES=CITIES', 'cities=CITIES')

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(c)
print("Replaced CITIES with cities in app.py")
