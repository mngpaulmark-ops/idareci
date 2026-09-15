with open('templates/admin/menu_list.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Add Status Header
text = text.replace('<th>Sıra</th>', '<th>Sıra</th>\n                <th>Durum</th>')

# Add Status Column and Toggle Button for Parent Menus
parent_status_td = '''<td>
                    {% if m.is_active %}
                    <span class="badge bg-success" style="background-color: green; padding: 5px; color: white; border-radius: 3px;">Aktif</span>
                    {% else %}
                    <span class="badge bg-secondary" style="background-color: gray; padding: 5px; color: white; border-radius: 3px;">Pasif</span>
                    {% endif %}
                </td>'''
text = text.replace('<td>{{ m.order }}</td>', f'<td>{{{{ m.order }}}}</td>\n                {parent_status_td}')

# Add Status Column and Toggle Button for Child Menus
child_status_td = '''<td>
                    {% if child.is_active %}
                    <span class="badge bg-success" style="background-color: green; padding: 5px; color: white; border-radius: 3px;">Aktif</span>
                    {% else %}
                    <span class="badge bg-secondary" style="background-color: gray; padding: 5px; color: white; border-radius: 3px;">Pasif</span>
                    {% endif %}
                </td>'''
text = text.replace('<td>{{ child.order }}</td>', f'<td>{{{{ child.order }}}}</td>\n                {child_status_td}')

# Add Toggle form for Parent Menus
parent_toggle_form = '''
                    <form action="{{ url_for('admin_menu_toggle', id=m.id) }}" method="POST" style="display:inline;">
                        <button type="submit" class="btn btn-sm btn-{% if m.is_active %}secondary{% else %}success{% endif %}">
                            {% if m.is_active %}Pasif Yap{% else %}Aktif Yap{% endif %}
                        </button>
                    </form>
'''
text = text.replace('<a href="{{ url_for(\'admin_menu_edit\', id=m.id) }}"', parent_toggle_form + '                    <a href="{{ url_for(\'admin_menu_edit\', id=m.id) }}"')

# Add Toggle form for Child Menus
child_toggle_form = '''
                        <form action="{{ url_for('admin_menu_toggle', id=child.id) }}" method="POST" style="display:inline;">
                            <button type="submit" class="btn btn-sm btn-{% if child.is_active %}secondary{% else %}success{% endif %}">
                                {% if child.is_active %}Pasif Yap{% else %}Aktif Yap{% endif %}
                            </button>
                        </form>
'''
text = text.replace('<a href="{{ url_for(\'admin_menu_edit\', id=child.id) }}"', child_toggle_form + '                        <a href="{{ url_for(\'admin_menu_edit\', id=child.id) }}"')

with open('templates/admin/menu_list.html', 'w', encoding='utf-8') as f:
    f.write(text)
print('Updated menu_list.html')
