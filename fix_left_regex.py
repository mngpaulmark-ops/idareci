with open('app.py', 'r', encoding='utf-8') as f:
    app_content = f.read()

import re

# Old pattern
old_pattern = r"pattern_left = r'(<div class=\"panel-heading\">\\s*<img alt=\"Menu\" src=\"themes/burokratlar/tema/images/icon-menu.png\"/> Derneğimiz\\s*</div>\\s*<div class=\"panel-body\">\\s*)<ul id=\"left-menu\">.*?</ul>(\\s*</div>)'"
old_replace = r"new_page = re.sub(pattern_left, r'\\g<1>' + left_html.replace('\\\\', '\\\\\\\\') + r'\\g<2>', new_page, flags=re.DOTALL)"

new_pattern = r"pattern_left = r'<ul id=\"left-menu\">.*?</ul>'"
new_replace = r"new_page = re.sub(pattern_left, left_html.replace('\\\\', '\\\\\\\\'), new_page, flags=re.DOTALL)"

app_content = app_content.replace(old_pattern, new_pattern)
app_content = app_content.replace(old_replace, new_replace)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(app_content)

print("Updated pattern_left in apply_menus_to_all_html")
