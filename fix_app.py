with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip = False
for line in lines:
    if line.strip() == "if __name__ == '__main__':" or line.strip() == 'if __name__ == "__main__":':
        skip = True
    elif skip and not line.startswith(' ') and not line.startswith('\t') and line.strip() != '':
        skip = False
        
    if not skip:
        new_lines.append(line)

new_lines.append('\nif __name__ == "__main__":\n')
new_lines.append('    with app.app_context():\n')
new_lines.append('        db.create_all()\n')
new_lines.append('    app.run(host="0.0.0.0", port=5005, debug=True)\n')

with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print('Fixed app.py')
