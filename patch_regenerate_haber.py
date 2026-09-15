import re

with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# I will replace the first 3 lines of regenerate_haber_html to also call haber_helper
target = """def regenerate_haber_html(haber):
    import subprocess
    subprocess.run(['python', 'update_anasayfa.py'])"""

replacement = """def regenerate_haber_html(haber):
    import subprocess
    subprocess.run(['python', 'update_anasayfa.py'])
    try:
        import haber_helper
        haber_helper.regenerate_haber_listesi()
    except Exception as e:
        print("Error regenerating haber listesi:", e)"""

new_code = code.replace(target, replacement)

if new_code != code:
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(new_code)
    print("Successfully patched regenerate_haber_html in app.py")
else:
    print("Could not find the target string in app.py")
