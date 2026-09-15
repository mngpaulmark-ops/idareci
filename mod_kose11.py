with open('import_kose11.py', 'r') as f:
    text = f.read()

text = text.replace('print("Extracted", len(tuples), "tuples")', 'print("in_string:", in_string)\n    print("Extracted", len(tuples), "tuples")')

with open('import_kose11.py', 'w') as f:
    f.write(text)
