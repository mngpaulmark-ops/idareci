import re

with open('app.py', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Fix admin_galeri_ekle
if 'import galeri_helper' not in content.split('def admin_galeri_ekle():')[1][:300]:
    content = content.replace(
        "def admin_galeri_ekle():\n    title = request.form.get('title')\n    db.session.add(Galeri(title=title))\n    db.session.commit()\n    return redirect(url_for('admin_galeri'))",
        "def admin_galeri_ekle():\n    title = request.form.get('title')\n    db.session.add(Galeri(title=title))\n    db.session.commit()\n    import galeri_helper\n    galeri_helper.regenerate_galleries()\n    return redirect(url_for('admin_galeri'))"
    )

# Fix admin_galeri_detay (POST part)
if 'galeri_helper.regenerate_galleries()' not in content.split('def admin_galeri_detay(id):')[1][:500]:
    content = content.replace(
        "db.session.commit()\n        return redirect(url_for('admin_galeri_detay', id=id))",
        "db.session.commit()\n        import galeri_helper\n        galeri_helper.regenerate_galleries()\n        return redirect(url_for('admin_galeri_detay', id=id))"
    )

# Fix admin_galeri_resimsil
if 'galeri_helper.regenerate_galleries()' not in content.split('def admin_galeri_resimsil(id):')[1][:300]:
    content = content.replace(
        "if r:\n        db.session.delete(r)\n    return redirect(url_for('admin_galeri_detay', id=gid))",
        "if r:\n        db.session.delete(r)\n        db.session.commit()\n        import galeri_helper\n        galeri_helper.regenerate_galleries()\n    return redirect(url_for('admin_galeri_detay', id=gid))"
    )

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Admin panel features patched in app.py")
