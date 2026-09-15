with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.read().split('\n')

for i, line in enumerate(lines):
    if line.strip() == "@app.route('/admin/settings', methods=['GET', 'POST'])":
        lines[i] = ""
    elif line.strip() == "def admin_settings():":
        lines[i] = "@app.route('/admin/settings', methods=['GET', 'POST'])\n" + line

with open('app.py', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
print('Fixed missing decorator for admin_settings')
