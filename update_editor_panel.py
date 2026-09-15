import re

with open('templates/admin/editor_panel.html', 'r', encoding='utf-8') as f:
    content = f.read()

new_block = '''{% if editor.can_kose %}
        <div class="col-md-4">
            <div class="card card-body bg-light mb-3">
                <h4>Köşe Yazıları Yönetimi</h4>
                <p>Köşe yazarlarını ve yazılarını yönetin.</p>
                <a href="{{ url_for('admin_kose') }}" class="btn btn-secondary">Yazılara Git</a>
            </div>
        </div>
        {% endif %}'''

content = content.replace('{% if editor.can_duyuru %}', new_block + '\n        {% if editor.can_duyuru %}')

with open('templates/admin/editor_panel.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated editor_panel.html")
