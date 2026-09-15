import re

with open('templates/admin/index.html', 'r', encoding='utf-8', errors='surrogateescape') as f:
    html = f.read()

# Replace the buttons area with a Jinja-conditional version!
buttons = """                <div>
                    {% if role == 'admin' %}
                        <a href="{{ url_for('admin_add') }}" class="btn btn-primary m-1">Sayfa Yönetimi (Ekle/Düzenle)</a>
                        <a href="{{ url_for('admin_temsilcilik') }}" class="btn btn-primary m-1">Temsilcilik Yönetimi</a>
                        <a href="{{ url_for('admin_yonkur') }}" class="btn btn-info m-1">Yönetim Kurulu & Kurullar</a>
                        <a href="{{ url_for('admin_galeri') }}" class="btn btn-primary m-1">Galeri Yönetimi</a>
                        <a href="{{ url_for('admin_menu') }}" class="btn btn-dark m-1">Menü Ayarları</a>
                        <a href="{{ url_for('admin_left_menu') }}" class="btn btn-secondary m-1">Sol Menü (Derneğimiz)</a>
                        <a href="{{ url_for('admin_editors') }}" class="btn btn-info m-1 text-white" style="background-color: #6f42c1; border-color: #6f42c1;">Yetkili / Editör Yönetimi</a>
                        <a href="{{ url_for('admin_settings') }}" class="btn btn-warning m-1">Genel Ayarları</a>
                        <a href="{{ url_for('admin_hesap') }}" class="btn btn-danger m-1">Şifre / Hesap Ayarları</a>
                    {% endif %}
                    
                    {% if role == 'admin' or (editor and editor.can_haber) %}
                        <a href="{{ url_for('admin_haber') }}" class="btn btn-success m-1">Haber Yönetimi</a>
                    {% endif %}
                    
                    {% if role == 'admin' or (editor and editor.can_etkinlik) %}
                        <a href="{{ url_for('admin_etkinlik') }}" class="btn btn-info m-1" style="background-color: #0dcaf0; color: #000;">Etkinlikler</a>
                    {% endif %}
                    
                    {% if role == 'admin' or (editor and editor.can_kose) %}
                        <a href="{{ url_for('admin_kose') }}" class="btn btn-secondary m-1 text-white">Köşe Yazıları</a>
                    {% endif %}
                    
                    {% if role == 'admin' or (editor and editor.can_duyuru) %}
                        <!-- Duyuru modülü için yer ayrılmıştır -->
                        <a href="#" class="btn btn-warning m-1 text-dark" onclick="alert('Duyuru modülü yakında aktif edilecektir.')">Duyurular</a>
                    {% endif %}
                </div>"""

# Remove the old div
html = re.sub(r'<div>\s*<a href="\{\{ url_for\(\'admin_add\'\).*?</div>', buttons, html, flags=re.DOTALL)

with open('templates/admin/index.html', 'w', encoding='utf-8', errors='surrogateescape') as f:
    f.write(html)
print("Updated admin index HTML with permission checks.")
