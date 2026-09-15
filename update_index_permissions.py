import re

with open('templates/admin/index.html', 'r', encoding='utf-8', errors='surrogateescape') as f:
    html = f.read()

# Remove old Galeri button from admin-only section
html = re.sub(r'<a href="\{\{ url_for\(\'admin_galeri\'\) \}\}"[^>]*>Galeri Y.*?netimi</a>\s*', '', html)

# We will add Galeri and Video buttons into the conditional permissions block
permissions_block = """
                    {% if role == 'admin' or (editor and editor.can_galeri) %}
                        <a href="{{ url_for('admin_galeri') }}" class="btn btn-primary m-1" style="background-color: #6f42c1; color: white;">Resim (Galeri) Yönetimi</a>
                    {% endif %}
                    
                    {% if role == 'admin' or (editor and editor.can_video) %}
                        <a href="{{ url_for('admin_videos') }}" class="btn btn-dark m-1">Video Yönetimi</a>
                    {% endif %}
                    """

if "admin_videos" not in html:
    html = re.sub(r'\{% if role == \'admin\' or \(editor and editor.can_duyuru\) %\}.*?\{% endif %\}', r'\g<0>' + permissions_block, html, flags=re.DOTALL)

with open('templates/admin/index.html', 'w', encoding='utf-8', errors='surrogateescape') as f:
    f.write(html)
print("Updated admin index HTML for Galeri and Video permissions.")
