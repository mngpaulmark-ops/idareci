import re

with open('templates/admin/menu.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = re.sub(
    r'<span>.*?\{\{ child\.title \}\}.*?</span>',
    '''<span>&#8627; 
        {% if not child.is_active %}<del class="text-muted">{% endif %}
        {{ child.title }}
        {% if not child.is_active %}</del> <span class="badge bg-warning text-dark">Pasif</span>{% endif %}
        <small class="text-muted">({{ child.url }})</small>
    </span>''', text)

with open('templates/admin/menu.html', 'w', encoding='utf-8') as f:
    f.write(text)
