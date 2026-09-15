with open('import_kose5.py', 'r') as f:
    text = f.read()

text = text.replace('pass', 'print("Error:", e)')

with open('import_kose5.py', 'w') as f:
    f.write(text)
