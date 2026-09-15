import zipfile

# 1. Read the old app.py from backup
with zipfile.ZipFile('C:/Users/turga/OneDrive/Desktop/bürokratlar birliği site yedeği/burokratlarbirligi_yedek_14.09.2026.zip') as z:
    old_app = z.read('app.py').decode('utf-8')

# 2. Extract the missing block from old app.py
# The missing block starts at: "def admin_temsilcilik_add():"
# And ends right before: "def apply_menus_to_all_html():"
start_idx = old_app.find('def admin_temsilcilik_add():')
end_idx = old_app.find('def apply_menus_to_all_html():')
missing_code = old_app[start_idx:end_idx]

# 3. Read the new app.py
with open('app.py', 'r', encoding='utf-8') as f:
    new_app = f.read()

# 4. In new app.py, replace the current "def admin_temsilcilik_add():" (if it exists) up to "def apply_menus_to_all_html():"
# Or if it doesn't exist, insert the missing code before "def apply_menus_to_all_html():"

if 'def admin_temsilcilik_add():' in new_app:
    new_start_idx = new_app.find('def admin_temsilcilik_add():')
    new_end_idx = new_app.find('def apply_menus_to_all_html():')
    final_app = new_app[:new_start_idx] + missing_code + new_app[new_end_idx:]
else:
    new_end_idx = new_app.find('def apply_menus_to_all_html():')
    final_app = new_app[:new_end_idx] + missing_code + new_app[new_end_idx:]

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(final_app)

print("Restored missing routes to app.py")
