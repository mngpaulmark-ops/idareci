with open('templates/admin/menu.html', 'r', encoding='utf-8') as f:
    text = f.read()

# For parents
text = text.replace(
    '<strong>{{ m.title }} <small class="text-muted">({{ m.url }})</small></strong>',
    '''<strong>
        {% if not m.is_active %}<del class="text-muted">{% endif %}
        {{ m.title }} 
        {% if not m.is_active %}</del> <span class="badge bg-warning text-dark">Pasif</span>{% endif %}
        <small class="text-muted">({{ m.url }})</small>
    </strong>'''
)

text = text.replace(
    '''<a href="{{ url_for('admin_menu_move', id=m.id, dir='down') }}" class="btn btn-sm btn-outline-secondary"><i class="fa fa-arrow-down"></i></a>''',
    '''<a href="{{ url_for('admin_menu_move', id=m.id, dir='down') }}" class="btn btn-sm btn-outline-secondary"><i class="fa fa-arrow-down"></i></a>
                                <form action="{{ url_for('admin_menu_toggle', id=m.id) }}" method="POST" class="d-inline">
                                    <button class="btn btn-sm {% if m.is_active %}btn-success{% else %}btn-secondary{% endif %} ms-2" title="Aktif/Pasif Yap">
                                        <i class="fa {% if m.is_active %}fa-eye{% else %}fa-eye-slash{% endif %}"></i>
                                    </button>
                                </form>'''
)

# For children
text = text.replace(
    '<span>&#8627; {{ child.title }} <small class="text-muted">({{ child.url }})</small></span>',
    '''<span>&#8627; 
        {% if not child.is_active %}<del class="text-muted">{% endif %}
        {{ child.title }}
        {% if not child.is_active %}</del> <span class="badge bg-warning text-dark">Pasif</span>{% endif %}
        <small class="text-muted">({{ child.url }})</small>
    </span>'''
)

text = text.replace(
    '''<a href="{{ url_for('admin_menu_move', id=child.id, dir='down') }}" class="btn btn-sm btn-outline-secondary"><i class="fa fa-arrow-down"></i></a>''',
    '''<a href="{{ url_for('admin_menu_move', id=child.id, dir='down') }}" class="btn btn-sm btn-outline-secondary"><i class="fa fa-arrow-down"></i></a>
                                        <form action="{{ url_for('admin_menu_toggle', id=child.id) }}" method="POST" class="d-inline">
                                            <button class="btn btn-sm {% if child.is_active %}btn-success{% else %}btn-secondary{% endif %} ms-2" title="Aktif/Pasif Yap">
                                                <i class="fa {% if child.is_active %}fa-eye{% else %}fa-eye-slash{% endif %}"></i>
                                            </button>
                                        </form>'''
)

# Fix unicode characters that got messed up in template (e.g. &#8627;)
text = text.replace('""', '&#8627;')

with open('templates/admin/menu.html', 'w', encoding='utf-8') as f:
    f.write(text)
print('Updated menu.html')
