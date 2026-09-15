import re

with open('templates/admin/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's just find the last </div></div> in the row and inject it before that.
new_box = '''
        <div class="col-md-3 mb-4">
            <div class="card bg-secondary text-white h-100 shadow">
                <div class="card-body text-center">
                    <i class="fa fa-list-ul fa-3x mb-3"></i>
                    <h5 class="card-title">Sol Menü (Derneğimiz)</h5>
                </div>
                <div class="card-footer bg-transparent border-top-0">
                    <a href="{{ url_for('admin_left_menu') }}" class="btn btn-light w-100">Yönetim</a>
                </div>
            </div>
        </div>'''

text = text.replace('<!-- Add more admin modules here -->', new_box + '\n<!-- Add more admin modules here -->')

with open('templates/admin/index.html', 'w', encoding='utf-8') as f:
    f.write(text)
print('Updated admin index via placeholder')
