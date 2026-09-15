import ast
c=open('fix_mojibake_all.py', 'r', encoding='utf-8').read()
d = ast.parse(c).body[2].value
for k, v in zip(d.keys, d.values):
    print(repr(k.value), "->", repr(v.value))
