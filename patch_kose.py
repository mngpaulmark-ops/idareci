import os

with open('app.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace db.session.commit() with db.session.commit() + generation call
# for the specific functions.
# A simpler way is to just do it wherever db.session.commit() happens inside those functions.
# Let's just find the exact places.
replacements = [
    ("        db.session.commit()\n        return redirect(url_for('admin_kose_list'))",
     "        db.session.commit()\n        os.system('python generate_kose.py')\n        os.system('python generate_kose_yazarlari.py')\n        return redirect(url_for('admin_kose_list'))"),
    
    ("    db.session.commit()\n    return redirect(url_for('admin_kose_list'))",
     "    db.session.commit()\n    os.system('python generate_kose.py')\n    os.system('python generate_kose_yazarlari.py')\n    return redirect(url_for('admin_kose_list'))"),
     
    ("        db.session.commit()\n        return redirect(url_for('yazar_panel'))",
     "        db.session.commit()\n        os.system('python generate_kose.py')\n        os.system('python generate_kose_yazarlari.py')\n        return redirect(url_for('yazar_panel'))"),
     
    ("    db.session.commit()\n    return redirect(url_for('yazar_panel'))",
     "    db.session.commit()\n    os.system('python generate_kose.py')\n    os.system('python generate_kose_yazarlari.py')\n    return redirect(url_for('yazar_panel'))")
]

for old, new in replacements:
    text = text.replace(old, new)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(text)
