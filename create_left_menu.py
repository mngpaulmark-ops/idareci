import re

with open('templates/admin/menu.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('Menü Yönetimi', 'Sol Menü (Derneğimiz) Yönetimi')
text = text.replace("url_for('admin_menu_add')", "url_for('admin_left_menu_add')")
text = text.replace("url_for('admin_menu_move'", "url_for('admin_left_menu_move'")
text = text.replace("url_for('admin_menu_toggle'", "url_for('admin_left_menu_toggle'")
text = text.replace("url_for('admin_menu_delete'", "url_for('admin_left_menu_delete'")

# Remove the parent select
text = re.sub(r'<div class="mb-3">[^<]*<label class="form-label">Üst Menü.*?</div>', '', text, flags=re.DOTALL|re.IGNORECASE)

# Or simpler: just remove the whole parent select block
text = re.sub(r'<select name="parent_id".*?</select>', '', text, flags=re.DOTALL)
text = re.sub(r'<label class="form-label">Üst Menü.*?<select', '<select', text, flags=re.DOTALL|re.IGNORECASE)
text = re.sub(r'<div class="mb-3">[\s\n]*<select', '<div style="display:none;"><select', text)

# Remove the children loop
text = re.sub(r'{% if m\.children %}.*?{% endif %}', '', text, flags=re.DOTALL)

with open('templates/admin/left_menu.html', 'w', encoding='utf-8') as f:
    f.write(text)
print('Created left_menu.html')
