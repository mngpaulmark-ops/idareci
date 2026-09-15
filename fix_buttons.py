with open('templates/admin/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

bad_string = """<a href="{{ url_for('admin_menu') }}" class="btn btn-dark m-1">
                    <a href="{{ url_for('admin_left_menu') }}" class="btn btn-secondary m-1">Sol Menü (Derneğimiz)</a>
MenǬ Ayarlar</a>"""

# Since encodings might cause mismatch, I will use regex to find and replace
import re
pattern = re.compile(r'<a href="\{\{ url_for\(\'admin_menu\'\) \}\}" class="btn btn-dark m-1">\s*<a href="\{\{ url_for\(\'admin_left_menu\'\) \}\}" class="btn btn-secondary m-1">Sol Menü \(Derneğimiz\)</a>\s*Men[^\<]+</a>')

replacement = """<a href="{{ url_for('admin_menu') }}" class="btn btn-dark m-1">Menü Ayarları</a>
                    <a href="{{ url_for('admin_left_menu') }}" class="btn btn-secondary m-1">Sol Menü (Derneğimiz)</a>"""

text = pattern.sub(replacement, text)

# Just in case the weird characters are different
pattern2 = re.compile(r'<a href="\{\{ url_for\(\'admin_menu\'\) \}\}" class="btn btn-dark m-1">\n\s*<a href="\{\{ url_for\(\'admin_left_menu\'\) \}\}" class="btn btn-secondary m-1">[^<]+</a>\n\s*[^<]+</a>', re.DOTALL)

text = pattern2.sub(replacement, text)

with open('templates/admin/index.html', 'w', encoding='utf-8') as f:
    f.write(text)
print('Fixed buttons')
