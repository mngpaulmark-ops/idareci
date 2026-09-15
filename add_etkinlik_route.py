import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

route_code = """
@app.route('/etkinlik.html')
@app.route('/etkinlikler.html')
def etkinlik_page():
    etkinlikler = Etkinlik.query.order_by(Etkinlik.id.desc()).all()
    return render_template('etkinlik_page.html', etkinlikler=etkinlikler)
"""

if "def etkinlik_page():" not in content:
    content = content.replace("@app.route('/<path:filename>')", route_code + "\n@app.route('/<path:filename>')")
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added route to app.py")
else:
    print("Route already exists")
