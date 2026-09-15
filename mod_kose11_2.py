with open('import_kose11.py', 'r') as f:
    text = f.read()

text = text.replace('print("in_string:", in_string)', 'print(current_val[-200:])\n    print("in_string:", in_string)')

with open('import_kose11.py', 'w') as f:
    f.write(text)
