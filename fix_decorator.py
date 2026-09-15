with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.read().split('\n')

for i, line in enumerate(lines):
    if line.strip() == "@app.route('/admin/haber')":
        lines[i] = ""
    elif line.strip() == "def admin_haber():":
        lines[i] = "@app.route('/admin/haber')\n" + line

with open('app.py', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
print('Fixed missing decorator for admin_haber')
