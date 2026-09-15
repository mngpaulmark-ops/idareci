import re

with open('templates/admin/widgets.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the heading of Kamu Etigi
pattern_kamu = r'<h4 class="text-primary mb-3"><i class="bi bi-mortarboard"></i> Kamu Etiği ve Yönetim İlkeleri</h4>'
repl_kamu = r'''<div class="d-flex justify-content-between align-items-center mb-3">
                                <h4 class="text-primary mb-0"><i class="bi bi-mortarboard"></i> Kamu Etiği ve Yönetim İlkeleri</h4>
                                <div class="form-check form-switch">
                                    <input class="form-check-input" type="checkbox" name="kamu_active" id="kamu_active" {% if kamu.is_active %}checked{% endif %} style="transform: scale(1.3);">
                                    <label class="form-check-label fw-bold ms-1" for="kamu_active">Aktif</label>
                                </div>
                            </div>'''
content = content.replace(pattern_kamu, repl_kamu)

# Replace the heading of Yonetim Liderlik
pattern_lider = r'<h4 class="text-danger mb-3"><i class="bi bi-person-workspace"></i> Yönetim ve Liderlik Seminerleri</h4>'
repl_lider = r'''<div class="d-flex justify-content-between align-items-center mb-3">
                                <h4 class="text-danger mb-0"><i class="bi bi-person-workspace"></i> Yönetim ve Liderlik Seminerleri</h4>
                                <div class="form-check form-switch">
                                    <input class="form-check-input" type="checkbox" name="lider_active" id="lider_active" {% if lider.is_active %}checked{% endif %} style="transform: scale(1.3);">
                                    <label class="form-check-label fw-bold ms-1" for="lider_active">Aktif</label>
                                </div>
                            </div>'''
content = content.replace(pattern_lider, repl_lider)

with open('templates/admin/widgets.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated widgets.html with active/passive switches.")
