import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r"(if ed\.can_etkinlik:\s*allowed_endpoints\.extend\(\['admin_etkinlik', 'admin_etkinlik_ekle', 'admin_etkinlik_edit', 'admin_etkinlik_sil'\]\))"
replacement = r"\1\n            if ed.can_kose:\n                allowed_endpoints.extend(['admin_kose', 'admin_yazar_ekle', 'admin_kose_ekle', 'admin_kose_edit', 'admin_kose_sil'])"

content = re.sub(pattern, replacement, content)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated app.py with allowed_endpoints for can_kose.")
