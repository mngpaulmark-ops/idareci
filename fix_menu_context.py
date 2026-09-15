import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# We need to wrap the body of apply_menus_to_all_html in with app.app_context():
# The definition is:
# def apply_menus_to_all_html():
#     import glob
#     import bs4
#     
#     # Generate Top Menu HTML
#     menus = Menu.query.filter_by(parent_id=None, is_active=True).order_by(Menu.order).all()
#     ...

# Instead of parsing all the indentation, let's just create a wrapper function.
# Wait, if I replace:
# def apply_menus_to_all_html():
# with:
# def _apply_menus_inner():
# and then add:
# def apply_menus_to_all_html():
#     with app.app_context():
#         _apply_menus_inner()

pattern = r'def apply_menus_to_all_html\(\):'
replacement = '''def _apply_menus_inner():'''

new_content = re.sub(pattern, replacement, content, count=1)

# Now append the wrapper function
wrapper = '''
def apply_menus_to_all_html():
    with app.app_context():
        _apply_menus_inner()
'''

new_content += wrapper

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Fixed apply_menus_to_all_html by adding app_context wrapper.")
