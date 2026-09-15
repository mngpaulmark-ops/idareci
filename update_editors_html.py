import re

with open('templates/admin/editors_list.html', 'r', encoding='utf-8', errors='surrogateescape') as f:
    html = f.read()

# Add to the "Add" form
add_check = """                <div class="mb-3 form-check">
                    <input type="checkbox" name="can_kose" class="form-check-input" id="ck">
                    <label class="form-check-label" for="ck">Köşe Yazısı Ekleme/Düzenleme Yetkisi</label>
                </div>
                <div class="mb-3 form-check">
                    <input type="checkbox" name="can_galeri" class="form-check-input" id="cg">
                    <label class="form-check-label" for="cg">Resim (Galeri) Ekleme/Düzenleme Yetkisi</label>
                </div>
                <div class="mb-3 form-check">
                    <input type="checkbox" name="can_video" class="form-check-input" id="cv">
                    <label class="form-check-label" for="cv">Video Link/Iframe Ekleme/Düzenleme Yetkisi</label>
                </div>"""
if 'name="can_galeri"' not in html:
    html = re.sub(r'<div class="mb-3 form-check">\s*<input type="checkbox" name="can_kose"[^>]*>\s*<label[^>]*>K.*?e Yaz.*?s.*? Ekleme/D.*?zenleme Yetkisi</label>\s*</div>', add_check, html, count=1)

# Add to the table badges
badges = """                    {% if ed.can_kose %}<span class="badge bg-secondary">Köşe Yazısı</span>{% endif %}
                    {% if ed.can_galeri %}<span class="badge bg-primary">Resim (Galeri)</span>{% endif %}
                    {% if ed.can_video %}<span class="badge bg-dark">Video</span>{% endif %}"""
if 'Resim (Galeri)' not in html:
    html = re.sub(r'\{% if ed\.can_kose %\}<span class="badge bg-secondary">K.*?e Yaz.*?s.*?</span>\{% endif %\}', badges, html, count=1)

# Add to the "Edit" form
edit_check = """                        <div class="mb-3 form-check">
                            <input type="checkbox" name="can_kose" class="form-check-input" {% if ed.can_kose %}checked{% endif %}>
                            <label class="form-check-label">Köşe Yazısı Yetkisi</label>
                        </div>
                        <div class="mb-3 form-check">
                            <input type="checkbox" name="can_galeri" class="form-check-input" {% if ed.can_galeri %}checked{% endif %}>
                            <label class="form-check-label">Resim (Galeri) Yetkisi</label>
                        </div>
                        <div class="mb-3 form-check">
                            <input type="checkbox" name="can_video" class="form-check-input" {% if ed.can_video %}checked{% endif %}>
                            <label class="form-check-label">Video (Iframe) Yetkisi</label>
                        </div>"""
html = re.sub(r'<div class="mb-3 form-check">\s*<input type="checkbox" name="can_kose"[^>]*>\s*<label[^>]*>K.*?e Yaz.*?s.*? Yetkisi</label>\s*</div>', edit_check, html, count=1)

with open('templates/admin/editors_list.html', 'w', encoding='utf-8', errors='surrogateescape') as f:
    f.write(html)
print("Updated editors_list.html")
