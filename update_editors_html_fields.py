import re

with open('templates/admin/editors_list.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ADD Form fields
add_fields = '''<div class="mb-3">
                    <label class="form-label">Kullanıcı Adı</label>
                    <input type="text" name="username" class="form-control" required>
                </div>
                <div class="mb-3">
                    <label class="form-label">Adı Soyadı</label>
                    <input type="text" name="full_name" class="form-control">
                </div>
                <div class="row">
                    <div class="col-md-6 mb-3">
                        <label class="form-label">Ünvanı (Örn: Prof. Dr.)</label>
                        <input type="text" name="title" class="form-control">
                    </div>
                    <div class="col-md-6 mb-3">
                        <label class="form-label">Görevi (Örn: Genel Sekreter)</label>
                        <input type="text" name="role" class="form-control">
                    </div>
                </div>
                <div class="mb-3">
                    <label class="form-label">Şifre</label>
                    <input type="password" name="password" class="form-control" required>
                </div>'''

content = re.sub(r'<div class="mb-3">\s*<label class="form-label">Kullanıcı Adı</label>.*?<input type="password" name="password" class="form-control" required>\s*</div>', add_fields, content, flags=re.DOTALL)


# EDIT Form fields
edit_fields = '''<div class="mb-3">
                            <label class="form-label">Kullanıcı Adı</label>
                            <input type="text" name="username" class="form-control" value="{{ ed.username }}" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Adı Soyadı</label>
                            <input type="text" name="full_name" class="form-control" value="{{ ed.full_name or '' }}">
                        </div>
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Ünvanı</label>
                                <input type="text" name="title" class="form-control" value="{{ ed.title or '' }}">
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Görevi</label>
                                <input type="text" name="role" class="form-control" value="{{ ed.role or '' }}">
                            </div>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Yeni Şifre (Değiştirmek istemiyorsanız boş bırakın)</label>
                            <input type="password" name="password" class="form-control">
                        </div>'''

content = re.sub(r'<div class="mb-3">\s*<label class="form-label">Kullanıcı Adı</label>.*?<input type="password" name="password" class="form-control">\s*</div>', edit_fields, content, flags=re.DOTALL)

# Add name to table
content = content.replace('<th>Kullanıcı Adı</th>', '<th>Kullanıcı Adı</th>\n                        <th>Adı Soyadı (Ünvan/Görev)</th>')
content = content.replace('<td>{{ ed.username }}</td>', '<td>{{ ed.username }}</td>\n                  <td>{{ ed.full_name or "-" }} <br><small class="text-muted">{{ ed.title or "" }} {{ ed.role or "" }}</small></td>')

with open('templates/admin/editors_list.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated editors_list.html with extra fields.")
