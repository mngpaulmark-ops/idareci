with open('app.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace("os.system('python generate_kose.py')\n    os.system('python generate_kose_yazarlari.py')", "")
text = text.replace("os.system('python generate_kose.py')\n        os.system('python generate_kose_yazarlari.py')", "")
text = text.replace("os.system('python generate_kose.py')", "")
text = text.replace("os.system('python generate_kose_yazarlari.py')", "")

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(text)
