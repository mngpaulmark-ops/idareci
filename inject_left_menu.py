import re

with open('templates/admin/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Just inject it before the last </div> in the main row
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
        </div>
'''

# Find the end of the first row
row_end = text.find('</div>\n</div>\n\n<script>')
if row_end != -1:
    text = text[:row_end] + new_box + text[row_end:]
    with open('templates/admin/index.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Updated admin index')
else:
    print('Could not find injection point. Trying fallback.')
    if 'Menü Yönetimi' in text:
        text = text.replace('Menü Yönetimi', 'Menü Yönetimi' + new_box)
        with open('templates/admin/index.html', 'w', encoding='utf-8') as f:
            f.write(text)
        print('Updated admin index via fallback')
    else:
        print('Failed entirely')
