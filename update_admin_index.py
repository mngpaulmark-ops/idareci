import re

with open('templates/admin/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

old_menu = r'<div class="col-md-3 mb-4">.*?Menü Yönetimi.*?</div>\s*</div>'
match = re.search(old_menu, text, re.DOTALL)
if match:
    new_box = '''        <div class="col-md-3 mb-4">
            <div class="card bg-secondary text-white h-100 shadow">
                <div class="card-body text-center">
                    <i class="fa fa-list-ul fa-3x mb-3"></i>
                    <h5 class="card-title">Sol Menü (Derneğimiz)</h5>
                </div>
                <div class="card-footer bg-transparent border-top-0">
                    <a href="{{ url_for('admin_left_menu') }}" class="btn btn-light w-100">Düzenle</a>
                </div>
            </div>
        </div>
        </div>'''
    text = text.replace(match.group(0), match.group(0).replace('</div>\s*</div>', '</div>') + '\n' + new_box)
    with open('templates/admin/index.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Updated admin index')
else:
    print('Match not found')
