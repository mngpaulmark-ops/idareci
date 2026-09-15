with open('templates/admin/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

new_button = '''
<div class="col-lg-3 col-md-6">
    <div class="panel panel-info">
        <div class="panel-heading">
            <div class="row">
                <div class="col-xs-3">
                    <i class="fa fa-list-alt fa-5x"></i>
                </div>
                <div class="col-xs-9 text-right">
                    <div class="huge">Yan</div>
                    <div>Blok Ayarları</div>
                </div>
            </div>
        </div>
        <a href="{{ url_for('admin_side_links') }}">
            <div class="panel-footer">
                <span class="pull-left">Detayları Gör</span>
                <span class="pull-right"><i class="fa fa-arrow-circle-right"></i></span>
                <div class="clearfix"></div>
            </div>
        </a>
    </div>
</div>
'''

if 'Yan Blok Ayarları' not in text:
    # Just insert it right after the Menü Ayarları button
    text = text.replace('<!-- Menü Ayarları Sonu -->', '<!-- Menü Ayarları Sonu -->\n' + new_button)

with open('templates/admin/index.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Dashboard updated")
