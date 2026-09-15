with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if line.strip().startswith('def admin_'):
        # Check if the previous line is @app.route but NOT @login_required
        if '@app.route' in new_lines[-1] and '@login_required' not in new_lines[-1]:
            # Some functions have multiple @app.route. We should insert @login_required right before def
            new_lines.append('@login_required\n')
    new_lines.append(line)

with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print('Added login_required to all admin routes')
