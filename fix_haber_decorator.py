with open('app.py', 'r', encoding='utf-8') as f:
    c = f.read()

# Fix admin_haber missing decorators
c = c.replace("def admin_haber():\n\n    habers =", "@app.route('/admin/haber')\n@login_required\ndef admin_haber():\n\n    habers =")

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(c)

print("Restored admin_haber decorators.")
