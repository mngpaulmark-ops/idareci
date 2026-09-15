with open('templates/admin/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

link = """
                <div class="col-lg-3 col-md-6">
                    <div class="panel panel-default">
                        <div class="panel-heading">
                            <div class="row">
                                <div class="col-xs-3">
                                    <i class="fa fa-key fa-5x"></i>
                                </div>
                                <div class="col-xs-9 text-right">
                                    <div>Şifre Değiştir</div>
                                </div>
                            </div>
                        </div>
                        <a href="/admin/password">
                            <div class="panel-footer">
                                <span class="pull-left">Admin Bilgilerini Güncelle</span>
                                <span class="pull-right"><i class="fa fa-arrow-circle-right"></i></span>
                                <div class="clearfix"></div>
                            </div>
                        </a>
                    </div>
                </div>
"""
if '/admin/password' not in text:
    text = text.replace('<!-- Yeni Modüller Buraya Eklenebilir -->', link + '\n<!-- Yeni Modüller Buraya Eklenebilir -->')
    with open('templates/admin/index.html', 'w', encoding='utf-8') as f:
        f.write(text)
