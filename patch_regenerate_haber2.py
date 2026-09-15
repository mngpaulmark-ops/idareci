import re

with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

pattern = r'(def regenerate_haber_html\(haber\):\s+import subprocess\s+subprocess\.run\(\[\'python\', \'update_anasayfa\.py\'\]\))'

replacement = r'\1\n\n    try:\n        import haber_helper\n        haber_helper.regenerate_haber_listesi()\n    except Exception as e:\n        pass'

new_code = re.sub(pattern, replacement, code)

if new_code != code:
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(new_code)
    print("Successfully patched regenerate_haber_html in app.py")
else:
    print("Could not find the pattern.")
