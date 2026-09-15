import zipfile
import re

with zipfile.ZipFile('C:/Users/turga/OneDrive/Desktop/bürokratlar birliği site yedeği/burokratlarbirligi_yedek_14.09.2026.zip') as z:
    backup_app = z.read('app.py').decode('utf-8')

# Re-apply Haber date sorting
backup_app = backup_app.replace("Haber.query.order_by(Haber.id.desc()).all()", "Haber.query.order_by(Haber.date.desc(), Haber.id.desc()).all()")

# Re-apply date parsing in admin_haber_add and admin_haber_edit
# Actually, I'll just replace the entire admin_haber_* blocks!
with open('app.py', 'r', encoding='utf-8') as f:
    current_app = f.read()

haber_start = current_app.find("@app.route('/admin/haber')")
haber_blocks = current_app[haber_start:]

backup_haber_start = backup_app.find("@app.route('/admin/haber')")

final_app = backup_app[:backup_haber_start] + haber_blocks

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(final_app)
print("Restored and merged app.py")
