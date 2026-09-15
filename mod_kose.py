with open('import_kose.py', 'r') as f:
    text = f.read()

text = text.replace('pass', 'print("Error:", e, "cols len:", len(cols)); break')

with open('import_kose.py', 'w') as f:
    f.write(text)
