import re
with open('templates/admin/galeri_list.html', 'r', encoding='utf-8') as f:
    c = f.read()

old_list = r'<div class="list-group">.*?</div>'
new_list = '''<div class="list-group">
                {% for g in galeriler %}
                <div class="list-group-item d-flex justify-content-between align-items-center">
                    <a href="{{ url_for('admin_galeri_detay', id=g.id) }}" class="text-decoration-none flex-grow-1 text-dark fw-bold">
                        {{ g.title }}
                        <span class="badge bg-secondary rounded-pill ms-2">{{ g.resimler|length }} Resim</span>
                    </a>
                    <div>
                        <a href="{{ url_for('admin_galeri_edit', id=g.id) }}" class="btn btn-sm btn-warning me-1">Düzenle</a>
                        <form method="POST" action="{{ url_for('admin_galeri_sil', id=g.id) }}" style="display:inline;" onsubmit="return confirm('Bu galeriyi ve içindeki tüm resimleri silmek istediðinize emin misiniz?');">
                            <button type="submit" class="btn btn-sm btn-danger">Sil</button>
                        </form>
                    </div>
                </div>
                {% endfor %}
            </div>'''
c = re.sub(old_list, new_list, c, flags=re.DOTALL)
with open('templates/admin/galeri_list.html', 'w', encoding='utf-8') as f:
    f.write(c)
