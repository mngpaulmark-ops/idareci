with open('app.py', 'r', encoding='utf-8') as f:
    text = f.read()

model_str = "parent_id = db.Column(db.Integer, db.ForeignKey('menu.id'), nullable=True)"
replacement = "parent_id = db.Column(db.Integer, db.ForeignKey('menu.id'), nullable=True)\n    is_active = db.Column(db.Boolean, default=True)"

text = text.replace(model_str, replacement)

# Now modify apply_menus_to_all_html to filter out inactive menus
query_str = "menus = Menu.query.filter_by(parent_id=None).order_by(Menu.order).all()"
query_replace = "menus = Menu.query.filter_by(parent_id=None, is_active=True).order_by(Menu.order).all()"
text = text.replace(query_str, query_replace)

child_loop_str = "for child in m.children:"
child_loop_replace = "for child in [c for c in m.children if c.is_active]:"
text = text.replace(child_loop_str, child_loop_replace)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(text)
print('Updated app.py Menu model and generator')
