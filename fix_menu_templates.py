import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# We need to change:
# for file in glob.glob('*.html') + glob.glob('haber/*.html'):
# to:
# for file in glob.glob('*.html') + glob.glob('haber/*.html') + glob.glob('templates/*.html'):

pattern = r"for file in glob\.glob\('\*\.html'\) \+ glob\.glob\('haber/\*\.html'\):"
replacement = "for file in glob.glob('*.html') + glob.glob('haber/*.html') + glob.glob('templates/*.html'):"

new_content = re.sub(pattern, replacement, content)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Updated apply_menus_to_all_html to include templates folder!")
