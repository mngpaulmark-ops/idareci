import re

# 1. Update galeri_list.html
with open('templates/admin/galeri_list.html', 'r', encoding='utf-8', errors='surrogateescape') as f:
    html = f.read()

add_form = """                <div class="mb-3">
                    <label>Galeri Başlığı</label>
                    <input type="text" name="title" class="form-control" required>
                </div>
                <div class="mb-3">
                    <label>Tarih (Örn: 16 Haziran 2016)</label>
                    <input type="text" name="date" class="form-control">
                </div>
                <div class="mb-3">
                    <label>Lokasyon (Örn: Ankara)</label>
                    <input type="text" name="location" class="form-control">
                </div>"""
html = re.sub(r'<div class="mb-3">\s*<label>Galeri Ba.*?l.*?</label>\s*<input type="text" name="title" class="form-control" required>\s*</div>', add_form, html)

with open('templates/admin/galeri_list.html', 'w', encoding='utf-8', errors='surrogateescape') as f:
    f.write(html)

# 2. Update galeri_detay.html
with open('templates/admin/galeri_detay.html', 'r', encoding='utf-8', errors='surrogateescape') as f:
    html2 = f.read()

edit_form = """    <div class="card mb-4">
        <div class="card-header">Galeri Bilgilerini Güncelle</div>
        <div class="card-body">
            <form action="{{ url_for('admin_galeri_detay', id=galeri.id) }}" method="POST">
                <div class="mb-3">
                    <label>Galeri Başlığı</label>
                    <input type="text" name="title" class="form-control" value="{{ galeri.title }}" required>
                </div>
                <div class="mb-3">
                    <label>Tarih</label>
                    <input type="text" name="date" class="form-control" value="{{ galeri.date or '' }}">
                </div>
                <div class="mb-3">
                    <label>Lokasyon</label>
                    <input type="text" name="location" class="form-control" value="{{ galeri.location or '' }}">
                </div>
                <button type="submit" class="btn btn-primary">Güncelle</button>
            </form>
        </div>
    </div>
    
    <div class="card mb-4">"""

html2 = html2.replace('<div class="card mb-4">', edit_form, 1)

with open('templates/admin/galeri_detay.html', 'w', encoding='utf-8', errors='surrogateescape') as f:
    f.write(html2)

print("Updated galeri_list.html and galeri_detay.html")
