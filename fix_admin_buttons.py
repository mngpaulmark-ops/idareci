import re

with open('templates/admin/index.html', 'r', encoding='utf-8', errors='surrogateescape') as f:
    html = f.read()

buttons_to_add = """
                        <a href="{{ url_for('admin_widgets') }}" class="btn btn-secondary m-1">Ön Yüz Widget (Kamu/Yönetim)</a>
                        <a href="{{ url_for('admin_sidebar') }}" class="btn btn-success m-1" style="background-color: #198754;">Yan Bloklar (E-Bülten vb)</a>
"""

if "admin_widgets" not in html:
    html = html.replace("""<a href="{{ url_for('admin_menu') }}" class="btn btn-dark m-1">Menü Ayarları</a>""", 
                        """<a href="{{ url_for('admin_menu') }}" class="btn btn-dark m-1">Menü Ayarları</a>""" + buttons_to_add)
    
with open('templates/admin/index.html', 'w', encoding='utf-8', errors='surrogateescape') as f:
    f.write(html)
print("Updated admin/index.html with widget and sidebar buttons")
