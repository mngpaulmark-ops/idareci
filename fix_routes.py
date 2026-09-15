with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    if line.strip() in ['@app.route("/admin/menu")', "@app.route('/admin/menu')"]:
        # Only keep it if the next non-empty line is 'def admin_menu():'
        is_correct = False
        for j in range(i+1, min(i+5, len(lines))):
            if lines[j].strip() == '':
                continue
            if 'def admin_menu(' in lines[j]:
                is_correct = True
                break
            else:
                break
        
        if is_correct:
            new_lines.append(line)
        else:
            print("Removed dangling route:", line.strip())
    else:
        new_lines.append(line)

with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Cleaned up routes.")
