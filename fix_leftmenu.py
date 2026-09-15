with open('app.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace("render_template('admin/leftmenu.html'", "render_template('admin/left_menu.html'")

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(text)
print('Fixed leftmenu template name')
