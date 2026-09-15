import re

with open('templates/admin/editors_list.html', 'r', encoding='utf-8', errors='surrogateescape') as f:
    html = f.read()

# 1. Clean up the ADD form by removing the broken Jinja blocks
# Find the exact broken block inside the Add form and replace it with just the correct add-form check
broken_add_block_pattern = r'<div class="mb-3 form-check">\s*<input type="checkbox" name="can_kose" class="form-check-input" \{% if ed\.can_kose %\}checked\{% endif %\}>\s*<label class="form-check-label">K.*?e Yaz.*?s.*? Yetkisi</label>\s*</div>\s*<div class="mb-3 form-check">\s*<input type="checkbox" name="can_galeri" class="form-check-input" \{% if ed\.can_galeri %\}checked\{% endif %\}>\s*<label class="form-check-label">Resim \(Galeri\) Yetkisi</label>\s*</div>\s*<div class="mb-3 form-check">\s*<input type="checkbox" name="can_video" class="form-check-input" \{% if ed\.can_video %\}checked\{% endif %\}>\s*<label class="form-check-label">Video \(Iframe\) Yetkisi</label>\s*</div>'

html = re.sub(broken_add_block_pattern, """<div class="mb-3 form-check">
                    <input type="checkbox" name="can_kose" class="form-check-input" id="ck">
                    <label class="form-check-label" for="ck">Köşe Yazısı Ekleme/Düzenleme Yetkisi</label>
                </div>""", html, count=1)

# 2. Add the proper checkboxes to the EDIT form
# We look for the duyuru checkbox in the edit modal to append the rest
edit_duyuru_pattern = r'<div class="mb-3 form-check">\s*<input type="checkbox" name="can_kose" class="form-check-input" \{% if ed\.can_kose %\}checked\{% endif %\}>\s*<label class="form-check-label">K.*?e Yaz.*?s.*? Yetkisi</label>\s*</div>'

proper_edit_boxes = """                        <div class="mb-3 form-check">
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

html = re.sub(edit_duyuru_pattern, proper_edit_boxes, html)

# 3. Ensure Table badges display them too
table_badges = """{% if ed.can_kose %}<span class="badge bg-secondary">Köşe Yazısı</span>{% endif %}
                    {% if ed.can_galeri %}<span class="badge bg-primary">Resim (Galeri)</span>{% endif %}
                    {% if ed.can_video %}<span class="badge bg-dark">Video</span>{% endif %}"""

html = re.sub(r'\{% if ed\.can_kose %\}<span class="badge bg-secondary">K.*?e Yaz.*?s.*?</span>\{% endif %\}', table_badges, html)

with open('templates/admin/editors_list.html', 'w', encoding='utf-8', errors='surrogateescape') as f:
    f.write(html)
print("editors_list.html fixed.")
