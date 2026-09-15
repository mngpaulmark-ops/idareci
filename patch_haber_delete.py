import re

with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

pattern = r'(def admin_haber_delete\(id\):.*?db\.session\.commit\(\))'
replacement = r'\1\n    import subprocess\n    subprocess.run(["python", "update_anasayfa.py"])\n    try:\n        import haber_helper\n        haber_helper.regenerate_haber_listesi()\n    except:\n        pass'

new_code = re.sub(pattern, replacement, code, flags=re.DOTALL)

if new_code != code:
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(new_code)
    print("Successfully patched admin_haber_delete in app.py")
else:
    print("Could not find the pattern.")
