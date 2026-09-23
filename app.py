
_template_base = None
def get_base_template():
    global _template_base
    if _template_base is None:
        with open('hakkimizda.html', 'r', encoding='utf-8', errors='ignore') as f:
            _template_base = f.read()
    return _template_base

def handle_dynamic_fallback(filename):
    import re
    if filename.startswith('data/') or filename.startswith('themes/'):
        file_path = os.path.join(app.root_path, filename)
        if os.path.exists(file_path):
            return send_from_directory(app.root_path, filename)
        return redirect('/' + filename)

    now = time.time()
    if filename in _page_cache and (now - _page_cache_time.get(filename, 0)) < CACHE_TTL_SECONDS:
        from flask import make_response
        resp = make_response(_page_cache[filename])
        resp.headers['Cache-Control'] = 'public, max-age=120, s-maxage=300, stale-while-revalidate=600'
        resp.headers['X-Cache'] = 'HIT'
        return resp

    if filename.startswith('kose-yazilari-') and filename.endswith('.html'):
        match = re.search(r'kose-yazilari-(\d+)\.html', filename)
        if match:
            k_id = match.group(1)
            yazi = KoseYazisi.query.get(k_id)
            if yazi:
                base = get_base_template()
                yazar = Yazar.query.get(yazi.yazar_id)
                y_name = yazar.name if yazar else "Bilinmeyen"
                y_pic = yazar.image_path if yazar and yazar.image_path else 'themes/burokratlar/tema/images/no-image.png'
                date_prefix = (yazi.date_added.strftime("%d.%m.%Y") + " - ") if (yazi.date_added and yazi.date_added.year > 2000) else ""
                import bs4
                soup = bs4.BeautifulSoup(base, 'html.parser')
                main_div = soup.find('div', class_='col-md-9')
                if main_div:
                    new_html = f'''<div class="col-md-9" id="main"><div class="main"><div class="panel panel-primary">
                    <div class="panel-heading">Görüş & Politika Notları / {date_prefix}{yazi.title}</div>
                    <div class="panel-body"><div class="col-md-12">
                    <div style="float: left; margin-right: 15px; margin-bottom: 15px; text-align: center;">
                    <a href="kose-yazar-{yazi.yazar_id}.html"><img src="{y_pic}" style="max-width: 150px; border-radius: 8px;"/><br/><b>{y_name}</b></a>
                    </div>
                    <h3>{date_prefix}{yazi.title}</h3><hr/><div class="content-text">{yazi.content}</div>
                    </div></div></div></div></div>'''
                    main_div.replace_with(bs4.BeautifulSoup(new_html, 'html.parser'))
                return inject_dynamic_html(filename, base_html=str(soup))
                
    elif filename.startswith('kose-yazar-') and filename.endswith('.html'):
        match = re.search(r'kose-yazar-(\d+)\.html', filename)
        if match:
            y_id = match.group(1)
            yazar = Yazar.query.get(y_id)
            if yazar:
                base = get_base_template()
                yazilar = KoseYazisi.query.filter_by(yazar_id=y_id).order_by(KoseYazisi.date_added.desc(), KoseYazisi.id.desc()).all()
                import bs4
                soup = bs4.BeautifulSoup(base, 'html.parser')
                main_div = soup.find('div', class_='col-md-9')
                if main_div:
                    y_pic = yazar.image_path if yazar.image_path else 'themes/burokratlar/tema/images/no-image.png'
                    def _ylink(y):
                        d_str = (y.date_added.strftime("%d.%m.%Y") + " - ") if (y.date_added and y.date_added.year > 2000) else ""
                        return f'<li><a href="kose-yazilari-{y.id}.html">{d_str}{y.title}</a></li>'
                    links = "".join([_ylink(y) for y in yazilar])
                    new_html = f'''<div class="col-md-9" id="main"><div class="main"><div class="panel panel-primary">
                    <div class="panel-heading">Görüş & Politika Notları / {yazar.name}</div>
                    <div class="panel-body"><div class="col-md-4">
                    <img src="{y_pic}" style="float: left; max-width: 100%; margin-bottom:10px; margin-right:10px; border-radius: 8px;"/><br/><h4><b>{yazar.name}</b></h4>
                    </div><div class="col-md-8"><br/><h4>Yazarın Yazıları:</h4><ul>{links}</ul></div>
                    </div></div></div></div>'''
                    main_div.replace_with(bs4.BeautifulSoup(new_html, 'html.parser'))
                return inject_dynamic_html(filename, base_html=str(soup))
                
    elif filename.startswith('haber/') and filename.endswith('.html'):
        match = re.search(r'haber/(\d+)-.*\.html', filename)
        if match:
            h_id = match.group(1)
            haber = Haber.query.get(h_id)
            if haber:
                base = get_base_template()
                import bs4
                soup = bs4.BeautifulSoup(base, 'html.parser')
                main_div = soup.find('div', class_='col-md-9')
                if main_div:
                    img_html = f'<img src="{haber.image_path}" class="img-responsive" style="margin-bottom:15px;"/>' if haber.image_path else ''
                    new_html = f'''<div class="col-md-9" id="main"><div class="main"><div class="panel panel-primary">
                    <div class="panel-heading">Haberler / {haber.title}</div>
                    <div class="panel-body"><div class="col-md-12">
                    {img_html}
                    <h3>{haber.title}</h3><hr/><div class="content-text">{haber.content}</div>
                    </div></div></div></div></div>'''
                    main_div.replace_with(bs4.BeautifulSoup(new_html, 'html.parser'))
                return inject_dynamic_html(filename, base_html=str(soup))
                
    elif filename.startswith('galeri-resimler-') and filename.endswith('.html'):
        match = re.search(r'galeri-resimler-(\d+)', filename)
        if match:
            g_id = match.group(1)
            galeri = Galeri.query.options(
                selectinload(Galeri.resimler).defer(GaleriResim.image_data)
            ).get(g_id)
            if galeri:
                base = get_base_template()
                import bs4
                soup = bs4.BeautifulSoup(base, 'html.parser')
                main_div = soup.find('div', class_='col-md-9')
                if main_div:
                    photos_html = ""
                    for r in galeri.resimler:
                        if r.image_path and (r.image_path.startswith('http://') or r.image_path.startswith('https://')):
                            img_src = r.image_path
                        elif r.image_path and r.image_path.startswith('files.catbox.moe'):
                            img_src = f"https://{r.image_path}"
                        elif r.image_path:
                            img_src = f"/{r.image_path}"
                        else:
                            img_src = f"/media/resim/{r.id}"
                        photos_html += f'''
                        <div class="col-md-4 col-sm-6 mb-4" style="margin-bottom:20px;">
                            <div class="thumbnail" style="border: 1px solid #ddd; padding: 5px; border-radius: 6px; background:#fff;">
                                <a href="{img_src}" target="_blank">
                                    <img src="{img_src}" alt="{galeri.title}" style="width: 100%; height: 180px; object-fit: cover; border-radius: 4px;"/>
                                </a>
                            </div>
                        </div>'''
                    if not photos_html:
                        photos_html = '<div class="col-12"><div class="alert alert-info">Bu galeride henüz resim bulunmuyor.</div></div>'
                    new_html = f'''<div class="col-md-9" id="main"><div class="main"><div class="panel panel-primary">
                    <div class="panel-heading">Fotoğraf Galerisi / {galeri.title}</div>
                    <div class="panel-body">
                    <h3>{galeri.title}</h3><hr/>
                    <div class="row">{photos_html}</div>
                    </div></div></div></div>'''
                    main_div.replace_with(bs4.BeautifulSoup(new_html, 'html.parser'))
                return inject_dynamic_html(filename, base_html=str(soup))
                
    from flask import abort
    abort(404)
from werkzeug.utils import secure_filename

import os
import builtins
import os

# 1. Patch open() to prevent Read-Only crashes on Vercel
original_open = builtins.open
def safe_open(file, mode='r', *args, **kwargs):
    if isinstance(mode, str) and ('w' in mode or 'a' in mode or '+' in mode):
        try:
            return original_open(file, mode, *args, **kwargs)
        except OSError:
            import io
            if 'b' in mode:
                return io.BytesIO()
            else:
                return io.StringIO()
    return original_open(file, mode, *args, **kwargs)
builtins.open = safe_open

# 2. Patch os.makedirs
original_makedirs = os.makedirs
def safe_makedirs(*args, **kwargs):
    try:
        original_makedirs(*args, **kwargs)
    except OSError:
        pass
os.makedirs = safe_makedirs


from werkzeug.datastructures import FileStorage
def dummy_save(self, *args, **kwargs):
    pass
FileStorage.save = dummy_save
import requests

def upload_to_catbox(file_obj):
    from flask import flash
    try:
        file_data = file_obj.read()
        resp = requests.post(
            'https://catbox.moe/user/api.php',
            data={'reqtype': 'fileupload'},
            files={'fileToUpload': (file_obj.filename, file_data, file_obj.content_type)},
            timeout=15
        )
        if resp.status_code == 200:
            url = resp.text.strip()
            return url.replace('https://', '').replace('http://', '')
        else:
            flash("Resim yukleme hatasi (Bulut reddetti): " + str(resp.status_code))
            return None
    except Exception as e:
        flash("Resim yukleme baglanti hatasi")
        return None


from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, jsonify, session

from flask_sqlalchemy import SQLAlchemy

from datetime import datetime



app = Flask(__name__)



CITIES = {
    'TR-01': 'Adana', 'TR-02': 'Adıyaman', 'TR-03': 'Afyonkarahisar', 'TR-04': 'Ağrı', 'TR-05': 'Amasya',
    'TR-06': 'Ankara', 'TR-07': 'Antalya', 'TR-08': 'Artvin', 'TR-09': 'Aydın', 'TR-10': 'Balıkesir',
    'TR-11': 'Bilecik', 'TR-12': 'Bingöl', 'TR-13': 'Bitlis', 'TR-14': 'Bolu', 'TR-15': 'Burdur',
    'TR-16': 'Bursa', 'TR-17': 'Çanakkale', 'TR-18': 'Çankırı', 'TR-19': 'Çorum', 'TR-20': 'Denizli',
    'TR-21': 'Diyarbakır', 'TR-22': 'Edirne', 'TR-23': 'Elazığ', 'TR-24': 'Erzincan', 'TR-25': 'Erzurum',
    'TR-26': 'Eskişehir', 'TR-27': 'Gaziantep', 'TR-28': 'Giresun', 'TR-29': 'Gümüşhane', 'TR-30': 'Hakkari',
    'TR-31': 'Hatay', 'TR-32': 'Isparta', 'TR-33': 'Mersin', 'TR-34': 'İstanbul', 'TR-35': 'İzmir',
    'TR-36': 'Kars', 'TR-37': 'Kastamonu', 'TR-38': 'Kayseri', 'TR-39': 'Kırklareli', 'TR-40': 'Kırşehir',
    'TR-41': 'Kocaeli', 'TR-42': 'Konya', 'TR-43': 'Kütahya', 'TR-44': 'Malatya', 'TR-45': 'Manisa',
    'TR-46': 'Kahramanmaraş', 'TR-47': 'Mardin', 'TR-48': 'Muğla', 'TR-49': 'Muş', 'TR-50': 'Nevşehir',
    'TR-51': 'Niğde', 'TR-52': 'Ordu', 'TR-53': 'Rize', 'TR-54': 'Sakarya', 'TR-55': 'Samsun',
    'TR-56': 'Siirt', 'TR-57': 'Sinop', 'TR-58': 'Sivas', 'TR-59': 'Tekirdağ', 'TR-60': 'Tokat',
    'TR-61': 'Trabzon', 'TR-62': 'Tunceli', 'TR-63': 'Şanlıurfa', 'TR-64': 'Uşak', 'TR-65': 'Van',
    'TR-66': 'Yozgat', 'TR-67': 'Zonguldak', 'TR-68': 'Aksaray', 'TR-69': 'Bayburt', 'TR-70': 'Karaman',
    'TR-71': 'Kırıkkale', 'TR-72': 'Batman', 'TR-73': 'Şırnak', 'TR-74': 'Bartın', 'TR-75': 'Ardahan',
    'TR-76': 'Iğdır', 'TR-77': 'Yalova', 'TR-78': 'Karabük', 'TR-79': 'Kilis', 'TR-80': 'Osmaniye',
    'TR-81': 'Düzce',
    'AZ': 'Azerbaycan', 'DE': 'Almanya', 'US': 'Amerika Birleşik Devletleri',
    'FR': 'Fransa', 'GB': 'İngiltere', 'NL': 'Hollanda', 'BE': 'Belçika',
    'AT': 'Avusturya', 'CH': 'İsviçre', 'IT': 'İtalya', 'RU': 'Rusya',
    'KZ': 'Kazakistan', 'UZ': 'Özbekistan', 'TM': 'Türkmenistan', 'KG': 'Kırgızistan',
    'CY': 'Kuzey Kıbrıs (KKTC)', 'BA': 'Bosna Hersek', 'MK': 'Makedonya',
    'AL': 'Arnavutluk', 'XK': 'Kosova', 'BG': 'Bulgaristan', 'GR': 'Yunanistan',
    'IQ': 'Irak', 'SY': 'Suriye', 'IR': 'İran', 'SA': 'Suudi Arabistan',
    'QA': 'Katar', 'AE': 'Birleşik Arap Emirlikleri', 'EG': 'Mısır', 'PK': 'Pakistan',
    'AF': 'Afganistan', 'IN': 'Hindistan', 'CN': 'Çin', 'JP': 'Japonya',
    'KR': 'Güney Kore', 'AU': 'Avustralya', 'CA': 'Kanada', 'BR': 'Brezilya',
    'ZA': 'Güney Afrika'
}



app.config['SECRET_KEY'] = 'supersecretkey123'

db_url = os.environ.get('DATABASE_URL', 'postgresql://neondb_owner:npg_PHdtr61ILkWz@ep-restless-feather-b25l03vt-pooler.c-6.eu-central-1.aws.neon.tech/neondb?sslmode=require')
if db_url.startswith('postgres://'):
    db_url = db_url.replace('postgres://', 'postgresql://', 1)
if '?' not in db_url:
    db_url += '?sslmode=require'
app.config['SQLALCHEMY_DATABASE_URI'] = db_url

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
}

app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'uploads')



import time



db = SQLAlchemy(app)













class Yazar(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    image_path = db.Column(db.String(255), nullable=True)

    username = db.Column(db.String(50), nullable=True)

    password = db.Column(db.String(50), nullable=True)



class KoseYazisi(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    yazar_id = db.Column(db.Integer, db.ForeignKey('yazar.id'), nullable=False)

    title = db.Column(db.String(200), nullable=False)

    content = db.Column(db.Text, nullable=False)

    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    

    yazar = db.relationship('Yazar', backref=db.backref('yazilar', lazy=True))



class Galeri(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(50))
    location = db.Column(db.String(100))
    date = db.Column(db.String(50))
    location = db.Column(db.String(100))

    

class GaleriResim(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    galeri_id = db.Column(db.Integer, db.ForeignKey('galeri.id'), nullable=False)

    image_path = db.Column(db.String(255), nullable=True)

    image_data = db.Column(db.LargeBinary, nullable=True)

    mimetype = db.Column(db.String(100), default='image/jpeg')

    galeri = db.relationship('Galeri', backref=db.backref('resimler', lazy=True))





class Temsilcilik(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    city_code = db.Column(db.String(10), nullable=False)

    city_name = db.Column(db.String(50), nullable=False)

    name = db.Column(db.String(100), nullable=False)

    phone = db.Column(db.String(50), nullable=True)

    image_path = db.Column(db.String(200), nullable=True)

    order = db.Column(db.Integer, default=0)



class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)

    url = db.Column(db.String(255), nullable=False, default='#')

    order = db.Column(db.Integer, default=0)

    parent_id = db.Column(db.Integer, db.ForeignKey('menu.id'), nullable=True)

    is_active = db.Column(db.Boolean, default=True)

    children = db.relationship('Menu', backref=db.backref('parent', remote_side=[id]), order_by='Menu.order')





class LeftMenu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)

    url = db.Column(db.String(255), nullable=False, default='#')

    order = db.Column(db.Integer, default=0)

    is_active = db.Column(db.Boolean, default=True)



class SideLink(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    category = db.Column(db.String(50)) # 'dijital', 'gundem', 'ebulten', 'faydali'

    title = db.Column(db.String(255))

    url = db.Column(db.String(255))

    badge = db.Column(db.String(100)) # Used for GÃ¼ndem badge, or Dijital color class

    order = db.Column(db.Integer, default=0)

    is_active = db.Column(db.Boolean, default=True)





class Etkinlik(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(255), nullable=False)

    description = db.Column(db.Text, nullable=True)

    edate = db.Column(db.String(50), nullable=True)

    saat = db.Column(db.String(50), nullable=True)
    location = db.Column(db.String(255), nullable=True)

    type = db.Column(db.String(50), default='meeting')

    link = db.Column(db.String(255), default='')



class Setting(db.Model):

    key = db.Column(db.String(100), primary_key=True)

    value = db.Column(db.Text, nullable=True)



class Haber(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(255), nullable=False)

    slug = db.Column(db.String(255), unique=True, nullable=False)

    content = db.Column(db.Text, nullable=True)

    image_path = db.Column(db.String(255), nullable=True)

    date = db.Column(db.DateTime, default=datetime.utcnow)



class Yonkur(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    grup = db.Column(db.String(50), default='ya') # ya, yy, da, dy

    ordernum = db.Column(db.Integer, default=1)

    name = db.Column(db.String(255))

    unvan = db.Column(db.String(255))

    image_path = db.Column(db.String(255))





class WidgetContent(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    slug = db.Column(db.String(50), unique=True)

    title = db.Column(db.String(100))

    description = db.Column(db.Text)

    link = db.Column(db.String(255))

    is_active = db.Column(db.Boolean, default=True)



class SidebarBlock(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    slug = db.Column(db.String(50), unique=True)

    title = db.Column(db.String(100))

    is_active = db.Column(db.Boolean, default=True)



class Video(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(255))

    embed_code = db.Column(db.Text)

    order = db.Column(db.Integer, default=0)




class Mesaj(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(100), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)


class Page(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    slug = db.Column(db.String(100), unique=True, nullable=False)

    title = db.Column(db.String(200), nullable=False)

    content_html = db.Column(db.Text, nullable=False)

    menu_order = db.Column(db.Integer, default=0)



# Create database tables if they don't exist

with app.app_context():

    db.create_all()

    if Page.query.count() == 0:

        db.session.add(Page(slug='hakkimizda', title='HakkÄ±mÄ±zda', content_html='<p>HakkÄ±mÄ±zda iÃ§erik...</p>', menu_order=1))

        db.session.add(Page(slug='tuzugumuz', title='TÃ¼zÃ¼ÄŸÃ¼mÃ¼z', content_html='<p>TÃ¼zÃ¼ÄŸÃ¼mÃ¼z...</p>', menu_order=2))

        db.session.commit()



def login_required(f):

    @wraps(f)

    def decorated_function(*args, **kwargs):

        if not session.get('logged_in'):

            return redirect(url_for('login'))

        return f(*args, **kwargs)

    return decorated_function



@app.route('/login', methods=['GET', 'POST'])

def login():

    if request.method == 'POST':

        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        

        s_user = Setting.query.get('admin_user')

        s_pass = Setting.query.get('admin_pass')

        admin_u = s_user.value.strip() if s_user and s_user.value else 'admin'

        admin_p = s_pass.value.strip() if s_pass and s_pass.value else '123456'

        

        if username == admin_u and password == admin_p:

            session['logged_in'] = True

            session['role'] = 'admin'

            session.pop('yazar_id', None)

            return redirect(url_for('admin_index'))

            

        
        editor = EditorUser.query.filter_by(username=username).first()
        from werkzeug.security import check_password_hash
        if editor and check_password_hash(editor.password, password):
            session['logged_in'] = True
            session['role'] = 'editor'
            session['editor_id'] = editor.id
            session.pop('yazar_id', None)
            return redirect(url_for('editor_panel'))
            
        yazar = Yazar.query.filter_by(username=username, password=password).first()

        if yazar and yazar.username:

            session['logged_in'] = True

            session['yazar_id'] = yazar.id

            return redirect(url_for('yazar_panel'))

            

        flash('HatalÄ± giriÅŸ')

    return render_template('login.html')



@app.route('/logout')

def logout():

    session.pop('logged_in', None)

    return redirect(url_for('login'))




@app.route('/editor_panel')
@login_required
def editor_panel():
    if session.get('role') != 'editor':
        return redirect(url_for('admin_index'))
    editor = EditorUser.query.get(session.get('editor_id'))
    if not editor:
        return redirect(url_for('logout'))
    return render_template('admin/editor_panel.html', editor=editor)

@app.route('/admin')

@login_required

def admin_index():

    pages = Page.query.order_by(Page.menu_order).all()

    return render_template('admin/index.html', pages=pages)



@app.route('/admin/add', methods=['GET', 'POST'])

@login_required

def admin_add():

    if request.method == 'POST':

        title = request.form.get('title')

        slug = request.form.get('slug')

        content_html = request.form.get('content_html')

        menu_order = request.form.get('menu_order', type=int, default=0)

        

        new_page = Page(title=title, slug=slug, content_html=content_html, menu_order=menu_order)

        db.session.add(new_page)

        db.session.commit()

        

        # Yeni eklenen sayfa iin fiziksel .html dosyasini "hakkimizda.html"i baz alarak olustur

        import os



        import bs4

        template_file = 'hakkimizda.html'

        new_filename = f"{slug}.html"

        if os.path.exists(template_file):

            html = open(template_file, encoding='utf-8', errors='surrogateescape').read()

            soup = bs4.BeautifulSoup(html, 'html.parser')

            

            # basligi degistir

            panels = soup.find_all('div', class_='panel-heading')

            if panels:

                panels[-1].string = f"Ä°dareci ve BÃ¼rokratlar BirliÄŸi / {title}"

                

            # icerigi degistir

            body_panels = soup.find_all('div', class_='panel-body')

            if body_panels:

                content_div = body_panels[-1]

                box = content_div.find('div', class_='box')

                new_content = bs4.BeautifulSoup(content_html, 'html.parser')

                if box:

                    box.clear()

                    box.append(new_content)

                else:

                    content_div.clear()

                    content_div.append(new_content)

                    

            open(new_filename, 'w', encoding='utf-8', errors='surrogateescape').write(str(soup))

            

        flash('Sayfa baYaryla eklendi!')

        return redirect(url_for('admin_index'))

    return render_template('admin/edit.html', page=None)



@app.route('/admin/edit/<int:id>', methods=['GET', 'POST'])

@login_required

def admin_edit(id):

    page = Page.query.get_or_404(id)

    if request.method == 'POST':

        page.title = request.form.get('title')

        page.slug = request.form.get('slug')

        page.content_html = request.form.get('content_html')

        page.menu_order = request.form.get('menu_order', type=int, default=0)

        

        db.session.commit()

        

        # Sitenin statik yapisi korunsun diye fiziksel HTML dosyasina da yaz!

        import os



        import bs4

        filename = f"{page.slug}.html"

        if os.path.exists(filename):

            html = open(filename, encoding='utf-8', errors='surrogateescape').read()

            soup = bs4.BeautifulSoup(html, 'html.parser')

            panels = soup.find_all('div', class_='panel-body')

            if panels:

                content_div = panels[-1]

                box = content_div.find('div', class_='box')

                new_content = bs4.BeautifulSoup(page.content_html, 'html.parser')

                if box:

                    box.clear()

                    box.append(new_content)

                else:

                    content_div.clear()

                    content_div.append(new_content)

                

                open(filename, 'w', encoding='utf-8', errors='surrogateescape').write(str(soup))

        

        flash('Sayfa baYaryla gÇ¬ncellendi!')

        return redirect(url_for('admin_index'))

    return render_template('admin/edit.html', page=page)



@app.route('/admin/delete/<int:id>', methods=['POST'])

@login_required

def admin_delete(id):

    page = Page.query.get_or_404(id)

    db.session.delete(page)

    db.session.commit()

    

    import os



    filename = f"{page.slug}.html"

    if os.path.exists(filename):

        try:

            os.remove(filename)

        except Exception:

            pass

            

    flash('Sayfa baYaryla silindi!')

    return redirect(url_for('admin_index'))

    

@app.route('/api/menu')

def api_menu():

    pages = Page.query.order_by(Page.menu_order).all()

    return jsonify([{'title': p.title, 'slug': p.slug} for p in pages])



@app.route('/')

def index():

    return inject_dynamic_html('anasayfa.html')



@app.route('/dernegimiz/<slug>')

def view_page(slug):

    page = Page.query.filter_by(slug=slug).first_or_404()

    menu_pages = Page.query.order_by(Page.menu_order).all()

    return render_template('page.html', page=page, menu_pages=menu_pages)



@app.route('/idareci/')
@app.route('/idareci/<path:filename>')
def serve_idareci(filename=''):
    if not filename or filename == '/':
        return inject_dynamic_html('anasayfa.html')
    if filename.startswith('data/') or filename.startswith('themes/'):
        file_path = os.path.join(app.root_path, filename)
        if os.path.exists(file_path):
            return send_from_directory(app.root_path, filename)
        return redirect('/' + filename)
    file_path = os.path.join(app.root_path, filename)
    if os.path.exists(file_path):
        if file_path.endswith('.html'): return inject_dynamic_html(file_path)
        return send_from_directory(app.root_path, filename)
    elif os.path.exists(file_path + '.html'):
        return inject_dynamic_html(file_path + '.html')
    elif os.path.exists(file_path + '.htm'):
        return send_from_directory(app.root_path, filename + '.htm')
    else:
        return handle_dynamic_fallback(filename)

import time
from sqlalchemy import event
from sqlalchemy.orm import selectinload

_page_cache = {}
_page_cache_time = {}
_menu_cache = {'top': None, 'left': None, 'time': 0}
CACHE_TTL_SECONDS = 300  # 5 minutes

def clear_page_cache():
    _page_cache.clear()
    _page_cache_time.clear()
    _menu_cache['top'] = None
    _menu_cache['left'] = None
    _menu_cache['time'] = 0

try:
    @event.listens_for(db.session, 'after_commit')
    def auto_clear_cache_on_db_change(session):
        clear_page_cache()
except Exception:
    pass

def inject_dynamic_html(file_path, base_html=None):
    from flask import make_response
    cache_key = file_path
    if cache_key:
        now = time.time()
        if cache_key in _page_cache and (now - _page_cache_time.get(cache_key, 0)) < CACHE_TTL_SECONDS:
            resp = make_response(_page_cache[cache_key])
            resp.headers['Cache-Control'] = 'public, max-age=120, s-maxage=300, stale-while-revalidate=600'
            resp.headers['X-Cache'] = 'HIT'
            return resp

    if base_html:
        html = base_html
    else:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            html = f.read()
    try:
        import bs4
        soup = bs4.BeautifulSoup(html, 'html.parser')
        
        # 1 & 2. Inject Top Menu and Left Menu with in-memory cache
        now_time = time.time()
        if not _menu_cache.get('top') or (now_time - _menu_cache.get('time', 0)) > 600:
            all_menus = Menu.query.filter_by(is_active=True).order_by(Menu.order).all()
            parents = [m for m in all_menus if m.parent_id is None]
            children_map = {}
            for m in all_menus:
                if m.parent_id:
                    children_map.setdefault(m.parent_id, []).append(m)
            top_html = '<ul class="nav navbar-nav">\n<li class="home"><a href="anasayfa.html"><img alt="Ana Sayfa" src="themes/burokratlar/tema/images/ico-home.png"/></a></li>\n'
            for m in parents:
                ch = children_map.get(m.id, [])
                if ch:
                    top_html += f'<li class="dropdown"><a aria-expanded="false" class="dropdown-toggle" data-toggle="dropdown" href="{m.url}" role="button" target="_self">{m.title}</a>\n<ul class="dropdown-menu" role="menu">\n'
                    for child in ch:
                        top_html += f'<li><a href="{child.url}" target="_self">{child.title}</a></li>\n'
                    top_html += '</ul></li>\n'
                else:
                    top_html += f'<li><a href="{m.url}" target="_self">{m.title}</a></li>\n'
            top_html += '</ul>'
            _menu_cache['top'] = top_html

            left_menus = LeftMenu.query.filter_by(is_active=True).order_by(LeftMenu.order).all()
            left_html = '<ul id="left-menu">\n'
            for lm in left_menus: left_html += f'<li><a href="{lm.url}" target="_self">» {lm.title}</a></li>\n'
            left_html += '</ul>'
            _menu_cache['left'] = left_html
            _menu_cache['time'] = now_time

        nav_ul = soup.find('ul', class_='nav navbar-nav')
        if nav_ul and _menu_cache.get('top'):
            new_nav = bs4.BeautifulSoup(_menu_cache['top'], 'html.parser').ul
            if new_nav: nav_ul.replace_with(new_nav)

        left_ul = soup.find('ul', id='left-menu')
        if left_ul and _menu_cache.get('left'):
            new_left = bs4.BeautifulSoup(_menu_cache['left'], 'html.parser').ul
            if new_left: left_ul.replace_with(new_left)
            
        # 3. If this is anasayfa.html, inject Haberler, Duyurular, and Kose Yazilari
        if 'anasayfa.html' in file_path or 'index.html' in file_path:
            # Kose Yazilari (super-fast single DISTINCT ON query)
            kayan = soup.find('div', id='kayan_alan')
            if kayan:
                kayan_ul = kayan.find('ul')
                if kayan_ul:
                    all_y_map = {y.id: y for y in Yazar.query.all()}
                    latest_arts = KoseYazisi.query.distinct(KoseYazisi.yazar_id).order_by(KoseYazisi.yazar_id, KoseYazisi.date_added.desc(), KoseYazisi.id.desc()).all()
                    from datetime import datetime
                    yazilar = [(all_y_map[art.yazar_id], art) for art in latest_arts if art.yazar_id in all_y_map]
                    yazilar.sort(key=lambda item: (item[1].date_added if (item[1].date_added and item[1].date_added.year > 2000) else datetime.min, item[1].id), reverse=True)
                    kose_html = ""
                    for yazar, y in yazilar:
                        y_name = yazar.name if yazar else "Yazar"
                        y_pic = yazar.image_path if yazar and yazar.image_path else "themes/burokratlar/tema/images/no-image.png"
                        date_str = y.date_added.strftime("%d.%m.%Y") if (y.date_added and y.date_added.year > 2000) else ""
                        display_title = f"{date_str} - {y.title}" if date_str else y.title
                        kose_html += f'''<li class="kayan"><a href="kose-yazilari-{y.id}.html">
                        <img alt="{y_name}" class="yazar" src="{y_pic}" style=" border-radius: 10px;"/>
                        <p><b>{y_name}</b></p></a>
                        <span>{display_title}</span>
                        <div class="clearfix"></div></li>\n'''
                    kayan_ul.clear()
                    kayan_ul.append(bs4.BeautifulSoup(kose_html, 'html.parser'))
            
            # Haberler Slider
            slider = soup.find('ul', class_='slideshow')
            latest = Haber.query.order_by(Haber.date.desc(), Haber.id.desc()).limit(10).all()
            if slider:
                slider.clear()
                for h in latest:
                    img_src = h.image_path if h.image_path else 'data/haber/0.jpg'
                    li_html = f'<li><div class="title"><a href="haber/{h.id}-{h.slug}.html">{h.title}</a></div><a href="haber/{h.id}-{h.slug}.html"><img src="{img_src}" alt="{h.title}" /></a></li>'
                    slider.append(bs4.BeautifulSoup(li_html, 'html.parser'))
                    
            # Haberler List (news)
            news_panel = soup.find('div', class_='news')
            if news_panel:
                list_group = news_panel.find('div', class_='list-group')
                if list_group:
                    list_group.clear()
                    list_group['style'] = "height: 332px; overflow-y: auto; overflow-x: hidden; padding-right: 5px;"
                    panel_body = news_panel.find('div', class_='col-md-6')
                    if panel_body:
                        extra_groups = panel_body.find_all('div', class_='list-group')
                        for eg in extra_groups[1:]:
                            eg.decompose()
                    for h in latest[:5]:
                        img_src = h.image_path if h.image_path else 'data/haber/0.jpg'
                        item_html = f'<div class="col-md-3 list-group-left"><a href="haber/{h.id}-{h.slug}.html"><img src="{img_src}" class="img-responsive" loading="lazy"/></a></div><div class="col-md-9 list-group-right"><a href="haber/{h.id}-{h.slug}.html">{h.title}</a></div><div class="clearfix"></div>'
                        list_group.append(bs4.BeautifulSoup(item_html, 'html.parser'))
                        
            # Duyurular
            duyuru_ul = soup.find('ul', id='duyurular')
            if duyuru_ul:
                duyurular_db = Duyuru.query.order_by(Duyuru.date_added.desc(), Duyuru.id.desc()).limit(10).all()
                duyuru_html = ""
                for d in duyurular_db:
                    link = d.link if d.link else "#"
                    duyuru_html += f'<li class="news-item"><a href="{link}">{d.title}</a></li>\n'
                if not duyuru_html:
                    duyuru_html = '<li class="news-item"><a href="#">İdareci ve Bürokratlar Birliği Derneği Web Sitesine Hoşgeldiniz...</a></li>'
                duyuru_ul.clear()
                duyuru_ul.append(bs4.BeautifulSoup(duyuru_html, 'html.parser'))

            # Foto Galeri on anasayfa
            fotogaleri_div = soup.find('div', class_='fotogaleri')
            if fotogaleri_div:
                fg_ul = fotogaleri_div.find('ul')
                if fg_ul:
                    galeriler = Galeri.query.options(
                        selectinload(Galeri.resimler).defer(GaleriResim.image_data)
                    ).order_by(Galeri.id.desc()).limit(12).all()
                    if galeriler:
                        fg_html = ""
                        for g in galeriler:
                            cover_src = "themes/burokratlar/tema/images/no-image.png"
                            if g.resimler:
                                first_r = g.resimler[0]
                                if first_r.image_data:
                                    cover_src = f"/media/resim/{first_r.id}"
                                elif first_r.image_path and (first_r.image_path.startswith('http://') or first_r.image_path.startswith('https://')):
                                    cover_src = first_r.image_path
                                elif first_r.image_path and first_r.image_path.startswith('files.catbox.moe'):
                                    cover_src = f"https://{first_r.image_path}"
                                elif first_r.image_path:
                                    cover_src = f"/{first_r.image_path}"
                            elif os.path.exists(f"data/gallerygroup/{g.id}.jpg"):
                                cover_src = f"data/gallerygroup/{g.id}.jpg"
                            
                            fg_html += f'''<li>
                            <a class="center-image" href="galeri-resimler-{g.id}.html">
                            <img alt="{g.title}" class="img-rounded" src="{cover_src}" loading="lazy" style="width: 170px; height: 115px; object-fit: cover;"/>
                            <div class="caption">
                            <h5>{g.title}</h5>
                            </div>
                            </a>
                            </li>\n'''
                        fg_ul.clear()
                        fg_ul.append(bs4.BeautifulSoup(fg_html, 'html.parser'))

        # Resimler.html (Fotoğraf Galerisi)
        if 'resimler.html' in file_path:
            main_div = soup.find('div', id='main')
            if main_div:
                panel_body = main_div.find('div', class_='panel-body')
                row = panel_body.find('div', class_='row') if panel_body else None
                if row:
                    galeriler = Galeri.query.options(
                        selectinload(Galeri.resimler).defer(GaleriResim.image_data)
                    ).order_by(Galeri.id.desc()).all()
                    blocks = []
                    for g in galeriler:
                        cover_img = "themes/burokratlar/tema/images/no-image.png"
                        if g.resimler and len(g.resimler) > 0:
                            first_r = g.resimler[0]
                            if first_r.image_data:
                                cover_img = f"/media/resim/{first_r.id}"
                            elif first_r.image_path and (first_r.image_path.startswith('http://') or first_r.image_path.startswith('https://')):
                                cover_img = first_r.image_path
                            elif first_r.image_path and first_r.image_path.startswith('files.catbox.moe'):
                                cover_img = f"https://{first_r.image_path}"
                            elif first_r.image_path:
                                cover_img = f"/{first_r.image_path}"
                        elif os.path.exists(f"data/gallerygroup/{g.id}.jpg"):
                            cover_img = f"data/gallerygroup/{g.id}.jpg"
                            
                        date_str = g.date or ""
                        loc_str = g.location or ""
                        title_str = g.title or ""
                        
                        block = f'''<div class="col-md-4 mb-4" style="margin-bottom:20px; text-align:center;">
                            <div class="card" style="border: 1px solid #e0e0e0; border-radius: 8px; overflow: hidden; padding: 10px; background: #fff;">
                                <a href="galeri-resimler-{g.id}.html" style="text-decoration:none;">
                                    <img class="img-responsive rounded shadow" onerror="this.src='themes/burokratlar/tema/images/no-image.png'" src="{cover_img}" style="width:100%; height:200px !important; object-fit:cover !important; border-radius:8px;"/>
                                </a>
                                <div style="display: flex; justify-content: space-between; font-size: 12px; color: #888; margin-top: 10px; padding: 0 5px;">
                                    <span><i class="fa fa-calendar" style="color: #c00;"></i> {date_str}</span>
                                    <span><i class="fa fa-map-marker" style="color: #c00;"></i> {loc_str}</span>
                                </div>
                                <div style="text-align: center; margin-top: 10px; min-height: 45px;">
                                    <a href="galeri-resimler-{g.id}.html" style="color: #1a7bb9; text-decoration: none; font-size: 14px;">{title_str}</a>
                                </div>
                            </div>
                        </div>'''
                        blocks.append(block)
                    row.clear()
                    row.append(bs4.BeautifulSoup("\n".join(blocks), 'html.parser'))

        # kose-yazarlari.html
        if 'kose-yazarlari.html' in file_path:
            main_div = soup.find('div', id='main')
            if main_div:
                panel_body = main_div.find('div', class_='panel-body')
                if panel_body:
                    yazarlar_all = Yazar.query.all()
                    y_blocks = []
                    for yz in yazarlar_all:
                        if not yz.yazilar: continue
                        yz_pic = yz.image_path if yz.image_path else 'themes/burokratlar/tema/images/no-image.png'
                        y_blocks.append(f'''<div class="col-md-4" style="text-align: center; margin-bottom: 20px;">
                            <a href="kose-yazar-{yz.id}.html">
                                <img src="{yz_pic}" style="max-width: 150px; border-radius: 50%; height: 150px; object-fit: cover;" onerror="this.src=\'themes/burokratlar/tema/images/no-image.png\'"/>
                                <br/><b>{yz.name}</b>
                            </a>
                        </div>''')
                    if y_blocks:
                        panel_body.clear()
                        panel_body.append(bs4.BeautifulSoup("\n".join(y_blocks), 'html.parser'))

        # 4. Instant Hover Prefetcher for near 0ms page transitions
        if soup.body and not soup.find('script', id='instant-prefetch'):
            prefetch_js = '''<script id="instant-prefetch">
(function(){
    var p={};
    function f(u){
        if(!u||p[u]||u.indexOf('/admin')!==-1||u.indexOf('logout')!==-1)return;
        p[u]=1;
        var l=document.createElement('link');l.rel='prefetch';l.href=u;document.head.appendChild(l);
    }
    document.addEventListener('mouseover',function(e){var a=e.target.closest('a');if(a&&a.href&&a.origin===location.origin)f(a.href);},{passive:true});
    document.addEventListener('touchstart',function(e){var a=e.target.closest('a');if(a&&a.href&&a.origin===location.origin)f(a.href);},{passive:true});
})();
</script>'''
            soup.body.append(bs4.BeautifulSoup(prefetch_js, 'html.parser'))

        rendered_html = str(soup)
        if cache_key:
            _page_cache[cache_key] = rendered_html
            _page_cache_time[cache_key] = time.time()
        resp = make_response(rendered_html)
        resp.headers['Cache-Control'] = 'public, max-age=120, s-maxage=300, stale-while-revalidate=600'
        resp.headers['X-Cache'] = 'MISS'
        return resp
    except Exception as e:
        print(str(e))
        from flask import make_response
        resp = make_response(html)
        resp.headers['Cache-Control'] = 'public, max-age=120, s-maxage=300, stale-while-revalidate=600'
        return resp

@app.route('/media/resim/<int:id>')
def serve_db_image(id):
    r = GaleriResim.query.get_or_404(id)
    if r.image_data:
        from flask import Response
        resp = Response(r.image_data, mimetype=r.mimetype or 'image/jpeg')
        resp.headers['Cache-Control'] = 'public, max-age=31536000, immutable'
        return resp
    elif r.image_path:
        return redirect('/' + r.image_path)
    from flask import abort
    abort(404)

@app.route('/<path:filename>')
def serve_static(filename):
    file_path = os.path.join(app.root_path, filename)
    if os.path.exists(file_path):
        if file_path.endswith('.html'): return inject_dynamic_html(file_path)
        return send_from_directory(app.root_path, filename)
    elif os.path.exists(file_path + '.html'):
        return inject_dynamic_html(file_path + '.html')
    elif os.path.exists(file_path + '.htm'):
        return send_from_directory(app.root_path, filename + '.htm')
    else:
        return handle_dynamic_fallback(filename)





@app.route('/admin/upload', methods=['POST'])

@login_required

def admin_upload():

    from flask import request, jsonify

    import os



    import time

    from werkzeug.utils import secure_filename

    

    if 'file' not in request.files:

        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']

    if file.filename == '':

        return jsonify({'error': 'No selected file'}), 400

    if file:

        filename = secure_filename(file.filename)

        name, ext = os.path.splitext(filename)

        filename = f"{name}_{int(time.time())}{ext}"

        

        upload_folder = os.path.join(app.root_path, 'data', 'uploads')

        os.makedirs(upload_folder, exist_ok=True)

        file_path = os.path.join(upload_folder, filename)

        file.save(file_path)

        

        return jsonify({'location': f'/data/uploads/{filename}'})

    return jsonify({'error': 'Upload failed'}), 500







def regenerate_temsilcilik_html():
    import json, bs4, os
    reps = Temsilcilik.query.order_by(Temsilcilik.city_name).all()
    
    turkey_areas = []
    world_areas_dict = {}
    
    import json
    try:
        with open('countries_tr.json', 'r', encoding='utf-8') as f:
            all_countries = json.load(f)
            for code, name in all_countries.items():
                world_areas_dict[code] = {
                    "id": code,
                    "title": name
                }
    except Exception:
        pass
        
    list_html = ""
    
    for rep in reps:
        img_url = f"/{rep.image_path}" if rep.image_path else "/images/default-avatar.png"
        
        custom_data = f"<div style='text-align:center;'><img src='{img_url}' style='width:60px; height:60px; border-radius:50%; object-fit:cover; margin-bottom:5px;'><br><b>{rep.name}</b><br>{rep.phone or ''}</div>"
        
        if rep.city_code.startswith('TR-'):
            turkey_areas.append({
                "id": rep.city_code,
                "title": rep.city_name,
                "color": "rgba(0,201,181,0.8)",
                "customData": custom_data
            })
        else:
            if rep.city_code in world_areas_dict:
                world_areas_dict[rep.city_code]["color"] = "rgba(0,201,181,0.8)"
                world_areas_dict[rep.city_code]["customData"] = custom_data
            else:
                world_areas_dict[rep.city_code] = {
                    "id": rep.city_code,
                    "title": rep.city_name,
                    "color": "rgba(0,201,181,0.8)",
                    "customData": custom_data
                }
        
        list_html += f'''
        <div class="col-12 col-md-6 col-lg-4" style="margin-bottom:20px; display:flex;">
            <div class="card border-0 shadow-sm" style="background:#fff; border-radius:10px; padding:15px; display:flex; flex-direction:row; align-items:center; width:100%; border: 1px solid #f1f1f1;">
                <img src="{img_url}" style="width:70px; height:70px; border-radius:50%; object-fit:cover; margin-right:15px; border:2px solid #eaeaea;" onerror="this.src='/images/default-avatar.png'; this.onerror=null;">
                <div>
                    <h5 style="color:#800000; font-size:16px; font-weight:700; margin-bottom:5px;">{rep.name}</h5>
                    <div style="font-size:13px; color:#555; font-weight:500;">{rep.city_name} Temsilcisi</div>
                    <div style="font-size:13px; color:#777; margin-top:3px;"><i class="fa fa-phone"></i> {rep.phone or ''}</div>
                </div>
            </div>
        </div>
        '''
        
    world_areas = list(world_areas_dict.values())

    turkey_json = json.dumps(turkey_areas, ensure_ascii=False)
    world_json = json.dumps(world_areas, ensure_ascii=False)
    
    temsil_html = f'''
    <script type="text/javascript" src="themes/burokratlar/tema/js/ammap.js"></script>
    <script type="text/javascript" src="https://www.amcharts.com/lib/3/maps/js/turkeyLow.js"></script>
    <script type="text/javascript" src="https://www.amcharts.com/lib/3/maps/js/worldLow.js"></script>
    <script type="text/javascript">
            var commonSettings = {{
                    "type": "map",
                    "pathToImages": "http://www.amcharts.com/lib/3/images/",
                    "addClassNames": true,
                    "fontSize": 12,
                    "color": "#000000",
                    "projection": "mercator",
                    "backgroundAlpha": 1,
                    "backgroundColor": "rgba(255,255,255,1)",
                    "zoomControl": {{
                        "zoomControlEnabled": true,
                        "panControlEnabled": false,
                        "homeButtonEnabled": true
                    }},
                    "maintainAspectRatio": true,
                    "balloon": {{
                        "horizontalPadding": 15,
                        "borderAlpha": 0,
                        "borderThickness": 1,
                        "verticalPadding": 15
                    }},
                    "areasSettings": {{
                        "color": "#e0e0e0",
                        "outlineColor": "rgba(255,255,255,1)",
                        "rollOverOutlineColor": "rgba(255,255,255,1)",
                        "rollOverBrightness": 20,
                        "selectedBrightness": 20,
                        "selectable": true,
                        "unlistedAreasAlpha": 1,
                        "unlistedAreasColor": "#e0e0e0",
                        "balloonText": "<div style='font-size:14px;'><b>[[title]]</b></div><div style='margin-top:5px;'>[[customData]]</div>",
                        "unlistedAreasOutlineAlpha": 0
                    }},
                    "zoomControl": {{
                        "zoomControlEnabled": true,
                        "homeButtonEnabled": true,
                        "panControlEnabled": true,
                        "right": 10,
                        "bottom": 10,
                        "minZoomLevel": 0.25,
                        "gridHeight": 100,
                        "gridAlpha": 0.1,
                        "gridBackgroundAlpha": 0,
                        "gridColor": "#FFFFFF",
                        "draggerAlpha": 1,
                        "buttonCornerRadius": 2
                    }}
            }};
            
            var turkeyChart = AmCharts.makeChart("map", commonSettings);
            turkeyChart.dataProvider = {{
                "map": "turkeyLow",
                "getAreasFromMap": true,
                
                "areas": {turkey_json}
            }};
            
            var worldChart = AmCharts.makeChart("mapWorld", commonSettings);
            worldChart.dataProvider = {{
                "map": "worldLow",
                "getAreasFromMap": true,
                "areas": {world_json}
            }};
    </script>
    <style>
        .amcharts-balloon-div {{ z-index: 9999 !important; padding:10px !important; }}
        .ammap-container {{ width: 100%; height: 500px; }}
        @media (max-width: 768px) {{
            .ammap-container {{ height: 300px !important; margin: 0 auto !important; }}
        }}
    </style>
    <div class="main">
    <div class="panel panel-primary" style="margin-top:20px; border:none;">
    <div class="panel-body">
    <center>
    <h3 style="color:#800000; font-weight:bold; margin-bottom:20px;">Türkiye Temsilcilikleri</h3>
    </center>
    <div id="map" class="ammap-container" style="background:#f9f9f9; border:1px solid #eee; border-radius:10px; margin-bottom: 40px;"></div>
    
    <center>
    <h3 style="color:#800000; font-weight:bold; margin-bottom:20px;">Dünya Temsilcilikleri</h3>
    </center>
    <div id="mapWorld" class="ammap-container" style="background:#f9f9f9; border:1px solid #eee; border-radius:10px;"></div>
    
    <div class="row" style="margin-top:40px;">
        {list_html}
    </div>
    
    </div></div><div class="clearfix"></div></div>
    '''
    
    filename = 'temsilcilik.html'
    if os.path.exists('hakkimizda.html'):
        with open('hakkimizda.html', 'r', encoding='utf-8', errors='ignore') as f:
            soup = bs4.BeautifulSoup(f.read(), 'html.parser')
        panels = soup.find_all('div', class_='panel-body')
        if panels:
            content_div = panels[-1]
            box = content_div.find('div', class_='box')
            new_content = bs4.BeautifulSoup(temsil_html, 'html.parser')
            if box:
                box.clear()
                box.append(new_content)
            else:
                content_div.clear()
                content_div.append(new_content)
            headings = soup.find_all('div', class_='panel-heading')
            if headings:
                headings[-1].string = 'İdareci ve Bürokratlar Birliği / Temsilcilikler'
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(str(soup))
                
            slug = 'temsilcilik'
            page = Page.query.filter_by(slug=slug).first()
            if page:
                page.content = str(box) if box else str(panels[-1])
            db.session.commit()

def regenerate_yonkur_html():

    from collections import defaultdict

    import bs4, os

    groups = defaultdict(list)

    members = Yonkur.query.order_by(Yonkur.ordernum).all()

    for m in members:

        groups[m.grup].append({

            'name': m.name,

            'unvan': m.unvan,

            'image_path': m.image_path if m.image_path else 'images/default-avatar.png'

        })



    def generate_group_html(title, members_list):

        if not members_list: return ''

        html = f'<div class="panel-body"><center><h3 class="heading-1" style="margin-bottom:30px; margin-top:20px;"><span>{title}</span></h3></center><div class="row justify-content-center" style="display:flex; flex-wrap:wrap; justify-content:center; gap: 20px;">'

        for member in members_list:

            html += f"""

            <div class="col-12 col-md-4 col-lg-3" style="margin-bottom:30px; display:flex;">

                <div class="card border-0 shadow" style="background:#fff; border-radius:15px; padding:25px 15px; text-align:center; box-shadow:0 8px 20px rgba(0,0,0,0.08); width:100%; border: 1px solid #f1f1f1;">

                    <img src="/{member['image_path']}" style="width:130px; height:130px; border-radius:50%; object-fit:cover; margin:0 auto 20px auto; border:4px solid #eaeaea; box-shadow:0 4px 10px rgba(0,0,0,0.1);" onerror="this.src='images/default-avatar.png'; this.onerror=null;">

                    <h5 style="color:#800000; font-size:17px; font-weight:700; margin-bottom:8px; line-height:1.3;">{member['name']}</h5>

                    <div style="font-size:13px; color:#666; font-weight:500; min-height:40px;">{member['unvan']}</div>

                </div>

            </div>

            """

        html += '</div></div><div class="clearfix"></div>'

        return html



    def write_to_file_and_db(filename, html_content, title):

        if os.path.exists(filename):

            with open(filename, 'r', encoding='utf-8', errors='surrogateescape') as f:

                soup = bs4.BeautifulSoup(f.read(), 'html.parser')

            panels = soup.find_all('div', class_='panel-body')

            if panels:

                content_div = panels[-1]

                box = content_div.find('div', class_='box')

                new_content = bs4.BeautifulSoup(html_content, 'html.parser')

                if box:

                    box.clear()

                    box.append(new_content)

                else:

                    content_div.clear()

                    content_div.append(new_content)

                

                # Update title

                headings = soup.find_all('div', class_='panel-heading')

                if headings:

                    headings[-1].string = f'Ä°dareci ve BÃ¼rokratlar BirliÄŸi / {title}'



                with open(filename, 'w', encoding='utf-8', errors='surrogateescape') as f:

                    f.write(str(soup))

                

                slug = filename.replace('.html', '')

                page = Page.query.filter_by(slug=slug).first()

                if page:

                    page.content = str(box) if box else str(panels[-1])

                db.session.commit()

        else:

            print(f"Warning: {filename} does not exist. Using hakkimizda as template.")

            # Fallback to hakkimizda template if not exists

            if os.path.exists('hakkimizda.html'):

                with open('hakkimizda.html', 'r', encoding='utf-8', errors='surrogateescape') as f:

                    soup = bs4.BeautifulSoup(f.read(), 'html.parser')

                panels = soup.find_all('div', class_='panel-body')

                if panels:

                    content_div = panels[-1]

                    box = content_div.find('div', class_='box')

                    new_content = bs4.BeautifulSoup(html_content, 'html.parser')

                    if box:

                        box.clear()

                        box.append(new_content)

                    else:

                        content_div.clear()

                        content_div.append(new_content)

                    headings = soup.find_all('div', class_='panel-heading')

                    if headings:

                        headings[-1].string = f'Ä°dareci ve BÃ¼rokratlar BirliÄŸi / {title}'

                    with open(filename, 'w', encoding='utf-8', errors='surrogateescape') as f:

                        f.write(str(soup))

                    

                    slug = filename.replace('.html', '')

                    page = Page.query.filter_by(slug=slug).first()

                    if page:

                        page.content = str(box) if box else str(panels[-1])

                    db.session.commit()



    # 1. Yonetim Kurulu

    yonkur_html = '<div class="main"><div class="panel panel-primary">'

    yonkur_html += generate_group_html('YÃ¶netim Kurulu Ãœyelerimiz', groups['ya'])

    yonkur_html += generate_group_html('YÃ¶netim Kurulu Yedek Ãœyelerimiz', groups['yy'])

    yonkur_html += generate_group_html('Denetleme Kurulu Ãœyelerimiz', groups['da'])

    yonkur_html += generate_group_html('Denetleme Kurulu Yedek Ãœyelerimiz', groups['dy'])

    yonkur_html += '</div></div>'

    write_to_file_and_db('yonetimkurulu.html', yonkur_html, 'YÃ¶netim Kurulu')



    # 2. Baskanlik ve Birimler

    baskanlik_html = '<div class="main"><div class="panel panel-primary">'

    baskanlik_html += generate_group_html('BaÅŸkanlÄ±k ve Birimler', groups['br'])

    baskanlik_html += '</div></div>'

    write_to_file_and_db('baskanlik-ve-birimler.html', baskanlik_html, 'BaÅŸkanlÄ±k ve Birimler')



    # 3. Yuksek Istisare

    istisare_html = '<div class="main"><div class="panel panel-primary">'

    istisare_html += generate_group_html('YÃ¼ksek Ä°stiÅŸare ve Onur Kurulu', groups['is'])

    istisare_html += '</div></div>'

    write_to_file_and_db('yuksek-istisare-onur-kurulu-uyesi.html', istisare_html, 'YÃ¼ksek Ä°stiÅŸare ve Onur Kurulu')







    



@app.route('/admin/yonkur')

@login_required

def admin_yonkur():

    members = Yonkur.query.order_by(Yonkur.ordernum).all()

    return render_template('admin/yonkur_list.html', members=members)



@app.route('/admin/yonkur/add', methods=['GET', 'POST'])

@login_required

def admin_yonkur_add():

    if request.method == 'POST':

        import time

        from werkzeug.utils import secure_filename

        m = Yonkur()

        m.name = request.form['name']

        m.unvan = request.form['unvan']

        m.grup = request.form['grup']

        m.ordernum = int(request.form.get('ordernum', 1))

        

        file = request.files.get('file')

        if file and file.filename != '':

            filename = secure_filename(file.filename)

            name, ext = os.path.splitext(filename)

            filename = f"{name}_{int(time.time())}{ext}"

            upload_folder = os.path.join(app.root_path, 'data', 'yonkur_uploads')

            os.makedirs(upload_folder, exist_ok=True)

            file.save(os.path.join(upload_folder, filename))

            m.image_path = f'data/yonkur_uploads/{filename}'

        else:

            m.image_path = 'images/default-avatar.png'

            

        db.session.add(m)

        db.session.commit()

        regenerate_yonkur_html()

        flash('Ãœye eklendi!')

        return redirect(url_for('admin_yonkur'))

    return render_template('admin/yonkur_edit.html', member=None)



@app.route('/admin/yonkur/edit/<int:id>', methods=['GET', 'POST'])

@login_required

def admin_yonkur_edit(id):

    m = Yonkur.query.get_or_404(id)

    if request.method == 'POST':

        import time

        from werkzeug.utils import secure_filename

        m.name = request.form['name']

        m.unvan = request.form['unvan']

        m.grup = request.form['grup']

        m.ordernum = int(request.form.get('ordernum', 1))

        

        file = request.files.get('file')

        if file and file.filename != '':

            filename = secure_filename(file.filename)

            name, ext = os.path.splitext(filename)

            filename = f"{name}_{int(time.time())}{ext}"

            upload_folder = os.path.join(app.root_path, 'data', 'yonkur_uploads')

            os.makedirs(upload_folder, exist_ok=True)

            file.save(os.path.join(upload_folder, filename))

            m.image_path = f'data/yonkur_uploads/{filename}'

            

        db.session.commit()

        regenerate_yonkur_html()

        flash('Ãœye gÃ¼ncellendi!')

        return redirect(url_for('admin_yonkur'))

    return render_template('admin/yonkur_edit.html', member=m)



@app.route('/admin/yonkur/delete/<int:id>', methods=['POST'])

@login_required

def admin_yonkur_delete(id):

    m = Yonkur.query.get_or_404(id)

    db.session.delete(m)

    db.session.commit()

    regenerate_yonkur_html()

    flash('Ãœye silindi!')

    return redirect(url_for('admin_yonkur'))





















# ================= YAZAR & KÃ–ÅE YAZISI =================

@app.route('/admin/kose')

@login_required

def admin_kose():

    import time

    t0 = time.time()

    yazilar = KoseYazisi.query.options(db.defer(KoseYazisi.content), db.joinedload(KoseYazisi.yazar)).order_by(KoseYazisi.date_added.desc(), KoseYazisi.id.desc()).limit(50).all()

    print('Query 1 time:', time.time() - t0)

    t1 = time.time()

    yazarlar = Yazar.query.all()

    print('Query 2 time:', time.time() - t1)

    t2 = time.time()

    res = render_template('admin/kose_list.html', yazilar=yazilar, yazarlar=yazarlar)

    print('Render time:', time.time() - t2)

    return res





@app.route('/yazar_panel')

@login_required

def yazar_panel():

    if 'yazar_id' not in session:

        return redirect(url_for('admin_index'))

    yazar = Yazar.query.get(session['yazar_id'])

    yazilar = KoseYazisi.query.filter_by(yazar_id=yazar.id).options(db.defer(KoseYazisi.content)).order_by(KoseYazisi.date_added.desc(), KoseYazisi.id.desc()).all()

    return render_template('admin/yazar_panel.html', yazar=yazar, yazilar=yazilar)



@app.route('/yazar_panel/ekle', methods=['POST'])

@login_required

def yazar_panel_ekle():

    if 'yazar_id' not in session: return redirect(url_for('login'))

    title = request.form.get('title')

    content = request.form.get('content')

    db.session.add(KoseYazisi(title=title, content=content, yazar_id=session['yazar_id']))

    db.session.commit()

    

    return redirect(url_for('yazar_panel'))



@app.route('/yazar_panel/sil/<int:id>', methods=['POST'])

@login_required

def yazar_panel_sil(id):

    if 'yazar_id' not in session: return redirect(url_for('login'))

    y = KoseYazisi.query.get(id)

    if y and y.yazar_id == session['yazar_id']:

        db.session.delete(y)

        db.session.commit()

    

    return redirect(url_for('yazar_panel'))



@app.route('/admin/hesap', methods=['GET', 'POST'])

@login_required

def admin_hesap():

    if 'yazar_id' in session: return redirect(url_for('yazar_panel'))

    

    s_user = Setting.query.get('admin_user')

    s_pass = Setting.query.get('admin_pass')

    current_u = s_user.value if s_user else 'admin'

    current_p = s_pass.value if s_pass else '123456'

    

    if request.method == 'POST':

        new_u = request.form.get('username')

        new_p = request.form.get('password')

        

        if not s_user:

            s_user = Setting(key='admin_user', value=new_u)

            db.session.add(s_user)

        else:

            s_user.value = new_u

            

        if not s_pass:

            s_pass = Setting(key='admin_pass', value=new_p)

            db.session.add(s_pass)

        else:

            s_pass.value = new_p

            

        db.session.commit()

        return redirect(url_for('login'))

        

    return render_template('admin/hesap.html', u=current_u, p=current_p)

@app.route('/admin/kose/yazar_ekle', methods=['POST'])

@login_required

def admin_yazar_ekle():

    name = request.form.get('name')

    file = request.files.get('image')

    img_path = None

    if file and file.filename:

        filename = secure_filename(file.filename)

        save_dir = os.path.join(app.root_path, 'data', 'page')

        os.makedirs(save_dir, exist_ok=True)

        path = os.path.join(save_dir, filename)

        file.save(path)

        img_path = 'data/page/' + filename

    

    db.session.add(Yazar(name=name, image_path=img_path, username=request.form.get("username"), password=request.form.get("password")))

    db.session.commit()

    return redirect(url_for('admin_kose'))



@app.route('/admin/kose/ekle', methods=['POST'])
@login_required
def admin_kose_ekle():
    title = request.form.get('title')
    content = request.form.get('content')
    yazar_id = request.form.get('yazar_id')
    date_str = request.form.get('date_added')
    
    from datetime import datetime
    if date_str:
        try:
            d = datetime.strptime(date_str, '%Y-%m-%d')
        except:
            d = datetime.utcnow()
    else:
        d = datetime.utcnow()
        
    yeni_yazi = KoseYazisi(title=title, content=content, yazar_id=yazar_id, date_added=d)
    db.session.add(yeni_yazi)
    db.session.commit()
    
    import kose_helper
    kose_helper.regenerate_single_kose(yeni_yazi.id)
    kose_helper.regenerate_single_yazar(yeni_yazi.yazar_id)
    
    return redirect(url_for('admin_kose'))


from flask import flash
@app.route('/admin/kose/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_kose_edit(id):
    yazi = KoseYazisi.query.get(id)
    if not yazi:
        flash("Köşe yazısı bulunamadı! Belki silinmiş veya ID yanlış.", "danger")
        return redirect(url_for('admin_kose'))
    if request.method == 'POST':
        yazi.title = request.form.get('title')
        yazi.content = request.form.get('content')
        yazi.yazar_id = request.form.get('yazar_id')
        date_str = request.form.get('date_added')
        if date_str:
            from datetime import datetime
            yazi.date_added = datetime.strptime(date_str, '%Y-%m-%d')
        db.session.commit()
        
        import kose_helper
        kose_helper.regenerate_single_kose(yazi.id)
        kose_helper.regenerate_single_yazar(yazi.yazar_id)
        
        return redirect(url_for('admin_kose'))

    yazarlar = Yazar.query.all()

    return render_template('admin/kose_edit.html', yazi=yazi, yazarlar=yazarlar)



@app.route('/admin/kose/sil/<int:id>', methods=['POST'])
@login_required
def admin_kose_sil(id):
    y = KoseYazisi.query.get(id)
    if y:
        yazar_id = y.yazar_id
        db.session.delete(y)
        db.session.commit()
        
        import os, kose_helper
        filename = f"kose-yazilari-{id}.html"
        if os.path.exists(filename):
            try:
                os.remove(filename)
            except:
                pass
        kose_helper.regenerate_single_yazar(yazar_id)
        
    return redirect(url_for('admin_kose'))





# ================= GALERÄ° =================



@app.route('/admin/etkinlik')

@login_required

def admin_etkinlik():

    etkinlikler = Etkinlik.query.order_by(Etkinlik.id.desc()).all()

    return render_template('admin/etkinlik_list.html', etkinlikler=etkinlikler)



@app.route('/admin/etkinlik/ekle', methods=['GET', 'POST'])

@login_required

def admin_etkinlik_ekle():

    if request.method == 'POST':

        title = request.form.get('title')

        description = request.form.get('description')

        edate = request.form.get('edate')

        saat = request.form.get('saat')

        

        location = request.form.get('location')
        yeni = Etkinlik(title=title, description=description, edate=edate, saat=saat, location=location)

        db.session.add(yeni)

        db.session.commit()

        import etkinlik_helper

        etkinlik_helper.regenerate_anasayfa_etkinlikler()

        return redirect(url_for('admin_etkinlik'))

    return render_template('admin/etkinlik_edit.html', etkinlik=None)



@app.route('/admin/etkinlik/edit/<int:id>', methods=['GET', 'POST'])

@login_required

def admin_etkinlik_edit(id):

    etkinlik = Etkinlik.query.get_or_404(id)

    if request.method == 'POST':

        etkinlik.title = request.form.get('title')

        etkinlik.description = request.form.get('description')

        etkinlik.edate = request.form.get('edate')

        etkinlik.saat = request.form.get('saat')
        etkinlik.location = request.form.get('location')
        db.session.commit()

        import etkinlik_helper

        etkinlik_helper.regenerate_anasayfa_etkinlikler()

        return redirect(url_for('admin_etkinlik'))

    return render_template('admin/etkinlik_edit.html', etkinlik=etkinlik)



@app.route('/admin/etkinlik/sil/<int:id>', methods=['POST'])

@login_required

def admin_etkinlik_sil(id):

    etkinlik = Etkinlik.query.get_or_404(id)

    db.session.delete(etkinlik)

    db.session.commit()

    import etkinlik_helper

    etkinlik_helper.regenerate_anasayfa_etkinlikler()

    return redirect(url_for('admin_etkinlik'))





@app.route('/admin/galeri')

@login_required

def admin_galeri():

    galeriler = Galeri.query.all()

    return render_template('admin/galeri_list.html', galeriler=galeriler)



@app.route('/admin/galeri/ekle', methods=['POST'])

@login_required

def admin_galeri_ekle():

    title = request.form.get('title')

    g = Galeri(title=title)

    db.session.add(g)

    db.session.commit()
    import threading
    try:
        import galeri_helper
        threading.Thread(target=galeri_helper.regenerate_resimler_html).start()
    except:
        pass

    flash(f"'{title}' galerisi oluşturuldu. Şimdi resimleri ekleyebilirsiniz.", "success")

    return redirect(url_for('admin_galeri_edit', id=g.id))



@app.route('/admin/galeri/<int:id>', methods=['GET', 'POST'])

@login_required

def admin_galeri_detay(id):

    galeri = Galeri.query.get_or_404(id)

    if request.method == 'POST':

        files = request.files.getlist('images')

        for file in files:
            if file and file.filename:
                file_bytes = file.read()
                if file_bytes:
                    filename = secure_filename(file.filename)
                    mime = file.content_type or 'image/jpeg'
                    gr = GaleriResim(
                        galeri_id=id,
                        image_path=f"data/gallery/{filename}",
                        image_data=file_bytes,
                        mimetype=mime
                    )
                    db.session.add(gr)
        db.session.commit()

        return redirect(url_for('admin_galeri_detay', id=id))

        

    return render_template('admin/galeri_detay.html', galeri=galeri)



@app.route('/admin/galeri/resimsil/<int:id>', methods=['POST'])

@login_required

def admin_galeri_resimsil(id):

    r = GaleriResim.query.get(id)

    gid = r.galeri_id

    if r:

        db.session.delete(r)

        db.session.commit()

    if request.referrer and 'edit' in request.referrer:
        return redirect(url_for('admin_galeri_edit', id=gid))
    return redirect(url_for('admin_galeri_detay', id=gid))



@app.route("/admin/menu")

@login_required

def admin_menu():

    menus = Menu.query.filter_by(parent_id=None).order_by(Menu.order).all()

    return render_template('admin/menu.html', menus=menus)



@app.route('/admin/menu/add', methods=['POST'])

@login_required

def admin_menu_add():

    title = request.form.get('title')

    url = request.form.get('url')

    parent_id = request.form.get('parent_id', type=int)

    if parent_id == 0: parent_id = None

    

    order = Menu.query.filter_by(parent_id=parent_id).count()

    new_menu = Menu(title=title, url=url, parent_id=parent_id, order=order)

    db.session.add(new_menu)

    db.session.commit()

    

    import threading; threading.Thread(target=apply_menus_to_all_html).start()

    return redirect(url_for('admin_menu'))



@app.route('/admin/menu/toggle/<int:id>', methods=['POST'])

@login_required

def admin_menu_toggle(id):

    menu = Menu.query.get_or_404(id)

    menu.is_active = not menu.is_active

    db.session.commit()

    import threading; threading.Thread(target=apply_menus_to_all_html).start()

    flash(f"MenÃ¼ {'aktif' if menu.is_active else 'pasif'} duruma getirildi.")

    return redirect(url_for('admin_menu'))



@app.route('/admin/menu/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_menu_edit(id):
    if not check_editor_permission('menu'): return redirect(url_for('admin_index'))
    menu = Menu.query.get_or_404(id)
    if request.method == 'POST':
        menu.title = request.form.get('title')
        menu.url = request.form.get('url')
        parent_id = request.form.get('parent_id')
        if parent_id and parent_id != '0':
            menu.parent_id = int(parent_id)
        else:
            menu.parent_id = None
        db.session.commit()
        
        import threading
        def bg_update():
            apply_menus_to_all_html()
        threading.Thread(target=bg_update).start()
        
        return redirect(url_for('admin_menu'))
    
    menus = Menu.query.filter_by(parent_id=None).order_by(Menu.order).all()
    return render_template('admin/menu_edit.html', menu=menu, menus=menus)

@app.route('/admin/left_menu/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_left_menu_edit(id):
    if not check_editor_permission('menu'): return redirect(url_for('admin_index'))
    menu = LeftMenu.query.get_or_404(id)
    if request.method == 'POST':
        menu.title = request.form.get('title')
        menu.url = request.form.get('url')
        db.session.commit()
        
        import threading
        def bg_update():
            apply_menus_to_all_html()
        threading.Thread(target=bg_update).start()
        
        return redirect(url_for('admin_left_menu'))

@app.route('/admin/menu/delete/<int:id>', methods=['POST'])
@login_required
def admin_menu_delete(id):

    menu = Menu.query.get_or_404(id)

    # Delete children first

    for child in menu.children:

        db.session.delete(child)

    db.session.delete(menu)

    db.session.commit()

    

    import threading; threading.Thread(target=apply_menus_to_all_html).start()

    return redirect(url_for('admin_menu'))



@app.route('/admin/menu/move/<int:id>/<dir>')

@login_required

def admin_menu_move(id, dir):

    menu = Menu.query.get_or_404(id)

    # Find sibling

    if dir == 'up':

        sibling = Menu.query.filter_by(parent_id=menu.parent_id).filter(Menu.order < menu.order).order_by(Menu.order.desc()).first()

    else:

        sibling = Menu.query.filter_by(parent_id=menu.parent_id).filter(Menu.order > menu.order).order_by(Menu.order.asc()).first()

        

    if sibling:

        # Swap orders

        menu.order, sibling.order = sibling.order, menu.order

        db.session.commit()

        import threading; threading.Thread(target=apply_menus_to_all_html).start()

        

    return redirect(url_for('admin_menu'))





def apply_side_links_to_all_html():

    import glob

    import bs4

    

    dijital = SideLink.query.filter_by(category='dijital', is_active=True).order_by(SideLink.order).all()

    gundem = SideLink.query.filter_by(category='gundem', is_active=True).order_by(SideLink.order).all()

    ebulten = SideLink.query.filter_by(category='ebulten', is_active=True).first()

    faydali = SideLink.query.filter_by(category='faydali', is_active=True).order_by(SideLink.order).all()

    

    html = ''

    

    if dijital:

        html += '<div class="panel panel-kurumsal mb-4 side-dijital"><div class="panel-heading text-center font-bold" style="background:#0f2b48; color:white; padding: 10px;">Dijital Ä°ÅŸlemler PortalÄ±</div><div class="panel-body text-center p-4">'

        for item in dijital:

            color = item.badge if item.badge else '#800000'

            text_color = 'white' if color == '#800000' else '#0f2b48'

            html += f'<a class="btn btn-primary w-full mb-2" href="{item.url}" style="background:{color}; border:none; display:block; padding:8px; color:{text_color}; border-radius:4px; text-decoration:none;">{item.title}</a>'

        html += '</div></div>'

        

    if gundem:

        html += '<div class="panel panel-kurumsal mb-4 side-gundem"><div class="panel-heading text-center font-bold" style="background:#0f2b48; color:white; padding: 10px;">GÃ¼ndem & BuluÅŸmalar</div><div class="panel-body p-4"><ul class="list-none p-0 m-0 text-sm">'

        for item in gundem:

            badge_html = f'<span style="background:#800000; color:white; padding:2px 6px; border-radius:4px; font-size:12px;">{item.badge}</span>' if item.badge else ''

            html += f'<li class="border-b py-2 mb-2">{badge_html} <a href="{item.url}" style="color:#0f2b48; font-weight:bold; text-decoration:none;">{item.title}</a></li>'

        html += '</ul></div></div>'

        

    if ebulten:

        html += '<div class="panel panel-kurumsal mb-4 side-ebulten"><div class="panel-heading text-center font-bold" style="background:#0f2b48; color:white; padding: 10px;">' + ebulten.title + '</div><div class="panel-body text-center p-4"><input class="form-control mb-2 p-2 border rounded w-full" placeholder="E-Posta Adresiniz" style="width:100%; box-sizing:border-box;" type="email"/><button class="btn btn-primary w-full mt-2" style="background:#800000; border:none; padding:8px; color:white; border-radius:4px; width:100%;">Abone Ol</button></div></div>'

        

    if faydali:

        html += '<div class="panel panel-cyan links side-faydali"><div class="panel-heading"><img alt="Link" src="themes/burokratlar/tema/images/icon-link.png"/>FaydalÄ± BaÄŸlantÄ±lar</div><div class="panel-body"><ul>'

        for item in faydali:

            html += f'<li><i aria-hidden="true" class="fa fa-link"></i> <a href="{item.url}" target="_blank">{item.title}</a></li>'

        html += '</ul></div></div>'



    for file in glob.glob('*.html') + glob.glob('haber/*.html'):

        with open(file, 'r', encoding='utf-8', errors='surrogateescape') as f:

            content = f.read()

            

        soup = bs4.BeautifulSoup(content, 'html.parser')

        left_menu_div = soup.find('div', class_='left-menu')

        

        if left_menu_div:

            # We must remove all old side blocks. They don't have a class we can target specifically except we know their structure.

            # Easiest way: remove everything in left_menu_div EXCEPT the panel-primary (DerneÄŸimiz)

            panels_to_remove = left_menu_div.find_all('div', class_='panel', recursive=False)

            for p in panels_to_remove:

                if 'panel-primary' not in p.get('class', []):

                    p.decompose()

            

            # Now append the new html blocks

            new_blocks = bs4.BeautifulSoup(html, 'html.parser')

            for tag in list(new_blocks.contents):

                left_menu_div.append(tag)

                

            html_str = str(soup)
            replacements = {
                'Ã¼': 'ü', 'Ã¶': 'ö', 'Ã§': 'ç', 'ÄŸ': 'ğ', 'Ä±': 'ı', 'ÅŸ': 'ş',
                'Ãœ': 'Ü', 'Ã–': 'Ö', 'Ã‡': 'Ç', 'Äž': 'Ğ', 'Ä°': 'İ', 'Åž': 'Ş'
            }
            for bad, good in replacements.items(): html_str = html_str.replace(bad, good)
            with open(file, 'w', encoding='utf-8', errors='surrogateescape') as f:
                f.write(html_str)



def apply_menus_to_all_html():
    with app.app_context():
        import os


        import re
        menus = Menu.query.filter_by(parent_id=None, is_active=True).order_by(Menu.order).all()
        html = '<ul class="nav navbar-nav">\n'
        html += '<li class="home"><a href="anasayfa.html"><img alt="Ana Sayfa" src="themes/burokratlar/tema/images/ico-home.png"/></a></li>\n'
        for m in menus:
            if m.children:
                html += f'<li class="dropdown"><a aria-expanded="false" class="dropdown-toggle" data-toggle="dropdown" href="{m.url}" role="button" target="_self">{m.title}</a>\n<ul class="dropdown-menu" role="menu">\n'
                for child in [c for c in m.children if c.is_active]: html += f'<li><a href="{child.url}" target="_self">{child.title}</a></li>\n'
                html += '</ul></li>\n'
            else:
                html += f'<li><a href="{m.url}" target="_self">{m.title}</a></li>\n'
        html += '</ul>'
        
        left_menus = LeftMenu.query.filter_by(is_active=True).order_by(LeftMenu.order).all()
        left_html = '<ul id="left-menu">\n'
        for lm in left_menus: left_html += f'<li><a href="{lm.url}" target="_self">» {lm.title}</a></li>\n'
        left_html += '</ul>'
        
        files_to_update = []
        for root, dirs, files in os.walk('.'):
            if 'themes' in root or 'templates' in root or '__pycache__' in root or 'instance' in root:
                continue
            for file in files:
                if file.endswith('.html'):
                    files_to_update.append(os.path.join(root, file))
                    
        for file in files_to_update:
            try:
                with open(file, 'r', encoding='utf-8', errors='ignore') as f: page = f.read()
            except: continue
            new_page = page
            pattern_top = r'(<nav class="collapse navbar-collapse bs-navbar-collapse" id="bs-example-navbar-collapse-1">\s*)<ul class="nav navbar-nav">.*?</ul>(\s*</nav>)'
            new_page = re.sub(pattern_top, r'\g<1>' + html.replace('\\', '\\\\') + r'\g<2>', new_page, flags=re.DOTALL)
            pattern_left = r'<ul id="left-menu">.*?</ul>'
            new_page = re.sub(pattern_left, left_html.replace('\\', '\\\\'), new_page, flags=re.DOTALL)
            if new_page != page:
                with open(file, 'w', encoding='utf-8') as f: f.write(new_page)
@app.route('/admin/haber')
@login_required
def admin_haber():

    habers = Haber.query.order_by(Haber.date.desc(), Haber.id.desc()).all()

    return render_template('admin/haber_list.html', habers=habers)



@app.route('/admin/haber/add', methods=['GET', 'POST'])

@login_required

def admin_haber_add():

    if request.method == 'POST':

        title = request.form.get('title')

        slug = secure_filename(title.lower().replace(' ', '-').replace('Ä±', 'i').replace('ÄŸ', 'g').replace('Ã¼', 'u').replace('ÅŸ', 's').replace('Ã¶', 'o').replace('Ã§', 'c'))

        content = request.form.get('content')

        

        file = request.files.get('file')

        image_path = None

        if file and file.filename != '':

            filename = secure_filename(file.filename)

            catbox_path = upload_to_catbox(file)
            if catbox_path:
                image_path = catbox_path
            else:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_path = 'data/uploads/' + filename

            

        new_haber = Haber(title=title, slug=slug, content=content, image_path=image_path)

        db.session.add(new_haber)

        db.session.commit()

        

        regenerate_haber_html(new_haber)

        return redirect(url_for('admin_haber'))

    return render_template('admin/haber_edit.html', haber=None)



@app.route('/admin/haber/edit/<int:id>', methods=['GET', 'POST'])

@login_required

def admin_haber_edit(id):

    haber = Haber.query.get_or_404(id)

    if request.method == 'POST':

        haber.title = request.form.get('title')

        haber.content = request.form.get('content')

        date_str = request.form.get('date')

        if date_str:

            from datetime import datetime

            haber.date = datetime.strptime(date_str, '%Y-%m-%d')

        

        file = request.files.get('file')

        if file and file.filename != '':

            filename = secure_filename(file.filename)

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            haber.image_path = 'data/uploads/' + filename

            

        db.session.commit()

        regenerate_haber_html(haber)

        return redirect(url_for('admin_haber'))

    return render_template('admin/haber_edit.html', haber=haber)



@app.route('/admin/haber/delete/<int:id>', methods=['POST'])

@login_required

def admin_haber_delete(id):

    haber = Haber.query.get_or_404(id)

    # Try to delete the html file

    html_path = f"haber/{haber.id}-{haber.slug}.html"

    if os.path.exists(html_path):

        try:

            os.remove(html_path)

        except:

            pass

    db.session.delete(haber)

    db.session.commit()
    import subprocess
    subprocess.run(["python", "update_anasayfa.py"])
    try:
        import haber_helper
        haber_helper.regenerate_haber_listesi()
    except:
        pass

    return redirect(url_for('admin_haber'))



def regenerate_haber_html(haber):

    import subprocess

    subprocess.run(['python', 'update_anasayfa.py'])

    try:
        import haber_helper
        haber_helper.regenerate_haber_listesi()
    except Exception as e:
        pass



    # This will read a template and write a static HTML file

    import bs4

    

    html_path = f"haber/{haber.id}-{haber.slug}.html"

    

    # We will use an existing news file as template, e.g. haber/1-burokratlar-birligi-adanada.html

    # But wait, we need to make sure the template exists.

    template_path = 'haber/1-burokratlar-birligi-adanada.html'

    if not os.path.exists(template_path):

        print("Template not found!")

        return

        

    with open(template_path, 'r', encoding='utf-8', errors='surrogateescape') as f:

        soup = bs4.BeautifulSoup(f.read(), 'html.parser')

        

    # Find the title box

    h2 = soup.find('h2')

    if h2:

        h2.string = haber.title

        

    # Find content box

    content_div = soup.find('div', class_='content')

    if not content_div:

        # Fallback to looking for panel-body

        panels = soup.find_all('div', class_='panel-body')

        if panels:

            content_div = panels[-1]

            

    if content_div:

        # We need to construct new content

        new_content = ""

        if haber.image_path:

            new_content += f'<center><img src="/{haber.image_path}" style="max-width:100%; border-radius:8px; margin-bottom:20px;"></center>'

        new_content += haber.content

        

        # Clear existing paragraphs or content inside the box that is not the title

        # Actually it's safer to just replace the inner HTML of the specific box

        # Let's find the 'box' inside panel-body

        box = content_div.find('div', class_='box')

        if box:

            box.clear()

            box.append(bs4.BeautifulSoup(new_content, 'html.parser'))

        else:

            # Maybe just append to panel-body?

            pass

            

    with open(html_path, 'w', encoding='utf-8', errors='surrogateescape') as f:

        f.write(str(soup))











@app.route('/admin/temsilcilik')

@login_required

def admin_temsilcilik():

    reps = Temsilcilik.query.order_by(Temsilcilik.city_name).all()

    return render_template('admin/temsil_list.html', reps=reps)



@app.route('/admin/temsilcilik/add', methods=['GET', 'POST'])

@login_required

def admin_temsilcilik_add():

    if request.method == 'POST':

        city_code = request.form.get('city_code')

        name = request.form.get('name')

        phone = request.form.get('phone')

        

        city_name = CITIES.get(city_code, '')

        

        image = request.files.get('image')

        image_path = None

        if image and image.filename:

            filename = secure_filename(image.filename)

            unique_filename = f"temsilci_{int(time.time())}_{filename}"

            image.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))

            image_path = f"uploads/{unique_filename}"

            

        new_rep = Temsilcilik(city_code=city_code, city_name=city_name, name=name, phone=phone, image_path=image_path)

        db.session.add(new_rep)

        db.session.commit()

        regenerate_temsilcilik_html()

        flash('Temsilcilik eklendi.')

        return redirect(url_for('admin_temsilcilik'))

        

    return render_template('admin/temsil_form.html', cities=CITIES, rep=None)



@app.route('/admin/temsilcilik/edit/<int:id>', methods=['GET', 'POST'])

@login_required

def admin_temsilcilik_edit(id):

    rep = Temsilcilik.query.get_or_404(id)

    if request.method == 'POST':

        rep.city_code = request.form.get('city_code')

        rep.city_name = CITIES.get(rep.city_code, '')

        rep.name = request.form.get('name')

        rep.phone = request.form.get('phone')

        

        image = request.files.get('image')

        if image and image.filename:

            filename = secure_filename(image.filename)

            unique_filename = f"temsilci_{int(time.time())}_{filename}"

            image.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))

            rep.image_path = f"data/uploads/{unique_filename}"

            

        db.session.commit()

        regenerate_temsilcilik_html()

        flash('Temsilcilik gÃ¼ncellendi.')

        return redirect(url_for('admin_temsilcilik'))

        

    return render_template('admin/temsil_form.html', cities=CITIES, rep=rep)



@app.route('/admin/temsilcilik/delete/<int:id>', methods=['POST'])

@login_required

def admin_temsilcilik_delete(id):

    rep = Temsilcilik.query.get_or_404(id)

    db.session.delete(rep)

    db.session.commit()

    regenerate_temsilcilik_html()

    flash('Temsilcilik silindi.')

    return redirect(url_for('admin_temsilcilik'))







@app.route('/admin/password', methods=['GET', 'POST'])

@login_required

def admin_password():

    if session.get('role') != 'admin':

        return "Yetkisiz giri", 403

        

    if request.method == 'POST':

        new_user = request.form.get('username')

        new_pass = request.form.get('password')

        

        # We store admin credentials in session usually, but here they are hardcoded in app.py's login route as admin / 123456 unless we create a table.

        # Let's create an Admin model and update it, OR simpler, since they want to change it, let's create a setting for it.

        # setting table has keys.

        admin_user = Setting.query.filter_by(key='admin_username').first()

        admin_pass = Setting.query.filter_by(key='admin_password').first()

        

        if not admin_user:

            admin_user = Setting(key='admin_username', value=new_user)

            db.session.add(admin_user)

        else:

            admin_user.value = new_user

            

        if not admin_pass:

            admin_pass = Setting(key='admin_password', value=new_pass)

            db.session.add(admin_pass)

        else:

            admin_pass.value = new_pass

            

        db.session.commit()

        return redirect(url_for('admin_index'))

        

    # Get current

    admin_user = Setting.query.filter_by(key='admin_username').first()

    curr_user = admin_user.value if admin_user else 'admin'

    return render_template('admin/password.html', username=curr_user)



import kose_helper



@app.route('/admin/leftmenu')

@login_required

def admin_left_menu():

    menus = LeftMenu.query.order_by(LeftMenu.order).all()

    return render_template('admin/left_menu.html', menus=menus)



@app.route('/admin/leftmenu/add', methods=['POST'])

@login_required

def admin_left_menu_add():

    title = request.form.get('title')

    url = request.form.get('url', '#')

    if title:

        last = LeftMenu.query.order_by(LeftMenu.order.desc()).first()

        order = (last.order + 1) if last else 0

        m = LeftMenu(title=title, url=url, order=order)

        db.session.add(m)

        db.session.commit()

        import threading; threading.Thread(target=apply_menus_to_all_html).start()

        flash('Sol menÃ¼ baÅŸarÄ±yla eklendi.', 'success')

    return redirect(url_for('admin_left_menu'))



@app.route('/admin/leftmenu/toggle/<int:id>', methods=['POST'])

@login_required

def admin_left_menu_toggle(id):

    m = LeftMenu.query.get_or_404(id)

    m.is_active = not m.is_active

    db.session.commit()

    import threading; threading.Thread(target=apply_menus_to_all_html).start()

    flash('Durum gÃ¼ncellendi.', 'success')

    return redirect(url_for('admin_left_menu'))



@app.route('/admin/leftmenu/delete/<int:id>', methods=['POST'])

@login_required

def admin_left_menu_delete(id):

    m = LeftMenu.query.get_or_404(id)

    db.session.delete(m)

    db.session.commit()

    import threading; threading.Thread(target=apply_menus_to_all_html).start()

    flash('Silindi.', 'success')

    return redirect(url_for('admin_left_menu'))



@app.route('/admin/leftmenu/move/<int:id>/<dir>')

@login_required

def admin_left_menu_move(id, dir):

    m = LeftMenu.query.get_or_404(id)

    if dir == 'up':

        other = LeftMenu.query.filter(LeftMenu.order < m.order).order_by(LeftMenu.order.desc()).first()

    else:

        other = LeftMenu.query.filter(LeftMenu.order > m.order).order_by(LeftMenu.order.asc()).first()

    if other:

        m.order, other.order = other.order, m.order

        db.session.commit()

        import threading; threading.Thread(target=apply_menus_to_all_html).start()

    return redirect(url_for('admin_left_menu'))



@app.route('/admin/settings', methods=['GET', 'POST'])

@login_required

def admin_settings():

    if request.method == 'POST':

        import update_social_links

        fb = request.form.get('facebook')

        tw = request.form.get('twitter')

        import threading

        threading.Thread(target=update_social_links.update_links, args=(fb, tw)).start()

        from flask import flash, redirect, url_for

        flash('Sosyal medya linkleri gÃ¼ncellendi.', 'success')

        return redirect(url_for('admin_settings'))



    import bs4

    fb_link = '#'

    tw_link = '#'

    try:

        with open('anasayfa.html', 'r', encoding='utf-8', errors='surrogateescape') as f:

            soup = bs4.BeautifulSoup(f.read(), 'html.parser')

            fb_tag = soup.find('a', class_='facebook')

            if fb_tag: fb_link = fb_tag.get('href')

            tw_tag = soup.find('a', class_='twitter')

            if tw_tag: tw_link = tw_tag.get('href')

    except:

        pass



    settings = {

        'facebook': {'label': 'Facebook Adresi', 'value': fb_link},

        'twitter': {'label': 'Twitter Adresi', 'value': tw_link}

    }

    return render_template('admin/settings.html', settings=settings)






@app.route('/admin/duyuru')
@login_required
def admin_duyuru():
    duyurular = Duyuru.query.order_by(Duyuru.date_added.desc(), Duyuru.id.desc()).all()
    return render_template('admin/duyuru_list.html', duyurular=duyurular)

@app.route('/admin/duyuru/add', methods=['GET', 'POST'])
@login_required
def admin_duyuru_add():
    if request.method == 'POST':
        t = request.form.get('title')
        l = request.form.get('link')
        d = Duyuru(title=t, link=l)
        db.session.add(d)
        db.session.commit()
        
        # Regenerate front page
        try:
            import subprocess
            subprocess.run(['python', 'update_anasayfa.py'])
        except:
            pass
            
        flash('Duyuru eklendi.', 'success')
        return redirect(url_for('admin_duyuru'))
    return render_template('admin/duyuru_edit.html')

@app.route('/admin/duyuru/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_duyuru_edit(id):
    d = Duyuru.query.get_or_404(id)
    if request.method == 'POST':
        d.title = request.form.get('title')
        d.link = request.form.get('link')
        db.session.commit()
        
        # Regenerate front page
        try:
            import subprocess
            subprocess.run(['python', 'update_anasayfa.py'])
        except:
            pass
            
        flash('Duyuru güncellendi.', 'success')
        return redirect(url_for('admin_duyuru'))
    return render_template('admin/duyuru_edit.html', duyuru=d)

@app.route('/admin/duyuru/delete/<int:id>', methods=['POST'])
@login_required
def admin_duyuru_delete(id):
    d = Duyuru.query.get_or_404(id)
    db.session.delete(d)
    db.session.commit()
    
    # Regenerate front page
    try:
        import subprocess
        subprocess.run(['python', 'update_anasayfa.py'])
    except:
        pass
        
    flash('Duyuru silindi.', 'success')
    return redirect(url_for('admin_duyuru'))

# ================= EDITOR USER MODEL & ROUTES =================



class Duyuru(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    link = db.Column(db.String(255))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

class EditorUser(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(50), nullable=False, unique=True)

    password = db.Column(db.String(255), nullable=False)

    full_name = db.Column(db.String(255))

    title = db.Column(db.String(100))

    role = db.Column(db.String(100))

    can_haber = db.Column(db.Boolean, default=False)

    can_etkinlik = db.Column(db.Boolean, default=False)

    can_duyuru = db.Column(db.Boolean, default=False)

    can_kose = db.Column(db.Boolean, default=False)

    can_galeri = db.Column(db.Boolean, default=False)

    can_video = db.Column(db.Boolean, default=False)

    can_mesaj = db.Column(db.Boolean, default=False)



@app.route('/admin/editors', methods=['GET', 'POST'])

@login_required

def admin_editors():

    from werkzeug.security import generate_password_hash

    if request.method == 'POST':

        action = request.form.get('action')

        u = request.form.get('username')

        p = request.form.get('password')

        ch = request.form.get('can_haber') == 'on'

        ce = request.form.get('can_etkinlik') == 'on'

        cd = request.form.get('can_duyuru') == 'on'

        ck = request.form.get('can_kose') == 'on'

        cg = request.form.get('can_galeri') == 'on'

        cv = request.form.get('can_video') == 'on'

        cm = request.form.get('can_mesaj') == 'on'

        fn = request.form.get('full_name')

        ti = request.form.get('title')

        ro = request.form.get('role')



        if action == 'add':

            db.session.add(EditorUser(

                username=u, password=generate_password_hash(p),

                full_name=fn, title=ti, role=ro,

                can_haber=ch, can_etkinlik=ce, can_duyuru=cd, can_kose=ck,

                can_galeri=cg, can_video=cv, can_mesaj=cm))

        elif action == 'edit':

            eid = request.form.get('editor_id')

            ed = EditorUser.query.get(eid)

            ed.username = u

            ed.full_name = fn

            ed.title = ti

            ed.role = ro

            if p: ed.password = generate_password_hash(p)

            ed.can_haber = ch

            ed.can_etkinlik = ce

            ed.can_duyuru = cd

            ed.can_kose = ck

            ed.can_galeri = cg

            ed.can_video = cv

            ed.can_mesaj = cm

        db.session.commit()

        flash('Yetkili editör kaydedildi.', 'success')

        return redirect(url_for('admin_editors'))

    editors = EditorUser.query.all()

    return render_template('admin/editors_list.html', editors=editors)



@app.route('/admin/editors/delete/<int:id>', methods=['POST'])

@login_required

def admin_editors_delete(id):

    ed = EditorUser.query.get_or_404(id)

    db.session.delete(ed)

    db.session.commit()

    flash('EditÃ¶r silindi.', 'success')

    return redirect(url_for('admin_editors'))



# ================= VIDEO GALLERY =================

@app.route('/admin/videos', methods=['GET', 'POST'])

@login_required

def admin_videos():

    if request.method == 'POST':

        title = request.form.get('title')

        embed = request.form.get('embed_code')

        order = request.form.get('order', type=int, default=0)

        db.session.add(Video(title=title, embed_code=embed, order=order))

        db.session.commit()

        import threading

        threading.Thread(target=update_video_html).start()

        flash('Video baÅŸarÄ±yla eklendi.', 'success')

        return redirect(url_for('admin_videos'))

    videos = Video.query.order_by(Video.order).all()

    return render_template('admin/video_list.html', videos=videos)



@app.route('/admin/videos/delete/<int:id>', methods=['POST'])

@login_required

def admin_video_delete(id):

    v = Video.query.get_or_404(id)

    db.session.delete(v)

    db.session.commit()

    import threading

    threading.Thread(target=update_video_html).start()

    flash('Video baÅŸarÄ±yla silindi.', 'success')

    return redirect(url_for('admin_videos'))



# ================= WIDGETS =================

@app.route('/admin/widgets', methods=['GET', 'POST'])

@login_required

def admin_widgets():

    kamu = WidgetContent.query.filter_by(slug='kamu-etigi').first()

    lider = WidgetContent.query.filter_by(slug='yonetim-liderlik').first()

    if not kamu:

        kamu = WidgetContent(slug='kamu-etigi', title='Kamu EtiÄŸi', description='', link='', is_active=True)

        db.session.add(kamu)

    if not lider:

        lider = WidgetContent(slug='yonetim-liderlik', title='YÃ¶netim Seminerleri', description='', link='', is_active=True)

        db.session.add(lider)

    db.session.commit()



    if request.method == 'POST':

        kamu.description = request.form.get('kamu_desc')

        kamu.link = request.form.get('kamu_link')

        kamu.is_active = request.form.get('kamu_active') == 'on'

        lider.description = request.form.get('lider_desc')

        lider.link = request.form.get('lider_link')

        lider.is_active = request.form.get('lider_active') == 'on'

        db.session.commit()

        import threading

        threading.Thread(target=update_widgets_html).start()

        flash('Widget iÃ§erikleri baÅŸarÄ±yla gÃ¼ncellendi.', 'success')

        return redirect(url_for('admin_widgets'))

    return render_template('admin/widgets.html', kamu=kamu, lider=lider)



# ================= SIDEBAR BLOCKS =================

@app.route('/admin/sidebar', methods=['GET', 'POST'])

@login_required

def admin_sidebar():

    blocks_data = [

        ('hadis', 'GÃ¼nÃ¼n Hadis-i Åerifi'),

        ('dijital', 'Dijital Ä°ÅŸlemler PortalÄ±'),

        ('gundem', 'GÃ¼ndem & BuluÅŸmalar'),

        ('ebulten', 'E-BÃ¼lten & Politika NotlarÄ±'),

        ('faydali', 'FaydalÄ± BaÄŸlantÄ±lar'),

        ('banner', 'Milli Ä°rade Platformu Banner')

    ]

    for slug, title in blocks_data:

        if not SidebarBlock.query.filter_by(slug=slug).first():

            db.session.add(SidebarBlock(slug=slug, title=title, is_active=True))

    db.session.commit()



    blocks = SidebarBlock.query.order_by(SidebarBlock.id).all()

    if request.method == 'POST':

        for b in blocks:

            b.is_active = request.form.get(f'block_{b.slug}') == 'on'

        db.session.commit()

        import threading

        threading.Thread(target=update_sidebar_html).start()

        flash('Sol menÃ¼ blok gÃ¶rÃ¼nÃ¼rlÃ¼kleri gÃ¼ncellendi.', 'success')

        return redirect(url_for('admin_sidebar'))

    return render_template('admin/sidebar_blocks.html', blocks=blocks)





# ================= SAFE HTML UPDATER FUNCTIONS (regex-based, no bs4) =================



def _toggle_display(style, is_active):

    """Helper to add/remove display:none from a CSS style string."""

    import re

    if is_active:

        style = re.sub(r'display:\s*none\s*!important;?', '', style)

        style = re.sub(r'display:\s*none;?', '', style)

    else:

        if 'display: none' not in style:

            style += ' display: none !important;'

    return style.strip()



def update_widgets_html():
    with app.app_context():
        import glob, re
        kamu = WidgetContent.query.filter_by(slug='kamu-etigi').first()
        lider = WidgetContent.query.filter_by(slug='yonetim-liderlik').first()
        if not kamu or not lider: return

        for file in glob.glob('anasayfa.html'):
            with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                page = f.read()
            
            new_page = page
            for w in [kamu, lider]:
                panel_id = f'panel-{w.slug}'
                
                # Regex to match the opening div tag completely
                pattern = r'(<div[^>]*id="' + re.escape(panel_id) + r'"[^>]*>)'
                
                def make_replacer(widget):
                    def replacer(match):
                        tag = match.group(1)
                        if 'style="' in tag:
                            # Replace existing style
                            if widget.is_active:
                                tag = re.sub(r'style="([^"]*display:\s*none\s*!important;?[^"]*)"', r'style=""', tag)
                            else:
                                tag = re.sub(r'style="([^"]*)"', r'style=" display: none !important;"', tag)
                        else:
                            # Insert style
                            if not widget.is_active:
                                tag = tag.replace('>', ' style="display: none !important;">', 1)
                        return tag
                    return replacer

                new_page = re.sub(pattern, make_replacer(w), new_page)
                
            if new_page != page:
                with open(file, 'w', encoding='utf-8') as f:
                    f.write(new_page)


def update_sidebar_html():
    with app.app_context():
        import os, re
        blocks = {b.slug: b.is_active for b in SidebarBlock.query.all()}
        if not blocks: return
        
        files_to_update = []
        for root, dirs, files in os.walk('.'):
            if 'themes' in root or 'templates' in root or '__pycache__' in root or 'instance' in root:
                continue
            for file in files:
                if file.endswith('.html'):
                    files_to_update.append(os.path.join(root, file))
                    
        for file in files_to_update:
            try:
                with open(file, 'r', encoding='utf-8', errors='surrogateescape') as f:
                    page = f.read()
            except: continue
            new_page = page
            for slug, is_active in blocks.items():
                class_name = 'hadis-i-serif' if slug == 'hadis' else f'side-{slug}'
                pattern_no_style = r'(<div[^>]*class="[^"]*' + re.escape(class_name) + r'[^"]*"[^>]*)(\s*)(>)'
                def ensure_style(match):
                    if 'style=' in match.group(1): return match.group(0)
                    return match.group(1) + ' style=""' + match.group(3)
                new_page = re.sub(pattern_no_style, ensure_style, new_page)
                
                pattern = r'(<div[^>]*class="[^"]*' + re.escape(class_name) + r'[^"]*"[^>]*style=")([^"]*)(")'
                def make_replacer(active):
                    def replacer(match):
                        return match.group(1) + _toggle_display(match.group(2), active) + match.group(3)
                    return replacer
                new_page = re.sub(pattern, make_replacer(is_active), new_page)
            if new_page != page:
                with open(file, 'w', encoding='utf-8', errors='surrogateescape') as f:
                    f.write(new_page)
def update_video_html():
    with app.app_context():
        import glob, bs4, re
        videos = Video.query.order_by(Video.order).all()
        
        # 1. Update anasayfa.html ONLY if there are videos
        if videos:
            html = ""
            for v in videos:
                html += f"<li><div style='padding: 5px; text-align:center;'>{v.embed_code}<div class='caption' style='margin-top:5px;'><h5 style='font-size:13px; font-weight:bold; color:#333;'>{v.title}</h5></div></div></li>\n"
            for file in glob.glob('anasayfa.html'):
                with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                    page = f.read()
                pattern = r'(<div class="panel-body videogaleri jcarousel">\s*<ul>).*?(</ul>\s*</div>)'
                new_page = re.sub(pattern, r'\g<1>\n' + html + r'\g<2>', page, flags=re.DOTALL)
                if new_page != page:
                    with open(file, 'w', encoding='utf-8') as f:
                        f.write(new_page)
                    
        # 2. Update videolar.html
        videolar_html = ""
        if not videos:
            # Fallback to old dummy video blocks if database is empty
            for i in range(1, 5):
                videolar_html += f'''<div class="col-md-6 mb-4" style="margin-bottom:20px;">
                <div class="gallery-hover shadow" style="background:#000; height:200px; display:flex; align-items:center; justify-content:center; color:white; font-size:40px; border-radius:8px; cursor:pointer;">
                ►
                </div>
                <h4 class="text-center mt-2" style="text-align:center;">Video {i}</h4>
                </div>\n'''
        else:
            for v in videos:
                videolar_html += f'''<div class="col-md-6 mb-4" style="margin-bottom:20px;">
                    <div class="shadow" style="border-radius:8px; overflow:hidden;">
                        {v.embed_code}
                    </div>
                    <h4 class="text-center mt-2" style="text-align:center;">{v.title}</h4>
                </div>\n'''
                
        for file in glob.glob('videolar.html'):
            with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                page2 = f.read()
            soup = bs4.BeautifulSoup(page2, 'html.parser')
            main_div = soup.find('div', id='main')
            if main_div:
                panel_body = main_div.find('div', class_='panel-body')
                if panel_body:
                    row_div = panel_body.find('div', class_='row')
                    if row_div:
                        row_div.clear()
                        row_div.append(bs4.BeautifulSoup(videolar_html, 'html.parser'))
                        with open(file, 'w', encoding='utf-8') as f:
                            f.write(str(soup))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006)
@app.route('/ping')
def ping():
    return 'pong_neon_5'

@app.route('/files.catbox.moe/<path:filename>')
def catbox_proxy(filename):
    return redirect(f"https://files.catbox.moe/{filename}")


@app.route('/admin/backup')
@login_required
def admin_backup():
    import tempfile
    import zipfile
    import json
    import os
    from flask import send_file

    if session.get('role') != 'admin':
        return redirect(url_for('admin_index'))

    tmp_dir = tempfile.gettempdir()
    zip_path = os.path.join(tmp_dir, 'site_backup.zip')
    
    db_dump = {}
    for mapper in db.Model.registry.mappers:
        model = mapper.class_
        table_name = model.__tablename__
        db_dump[table_name] = []
        try:
            records = model.query.all()
            for r in records:
                row = {}
                for col in model.__table__.columns:
                    val = getattr(r, col.name)
                    if isinstance(val, (int, float, str, bool, type(None))):
                        row[col.name] = val
                    else:
                        row[col.name] = str(val)
                db_dump[table_name].append(row)
        except Exception as e:
            pass
            
    db_json_path = os.path.join(tmp_dir, 'database_backup.json')
    with open(db_json_path, 'w', encoding='utf-8') as f:
        json.dump(db_dump, f, ensure_ascii=False, indent=2)
        
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.write(db_json_path, 'database_backup.json')
        for root, dirs, files in os.walk(app.root_path):
            if '.git' in root or '__pycache__' in root or '.venv' in root or 'venv' in root:
                continue
            for file in files:
                if file.endswith('.pyc'): continue
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, app.root_path)
                try:
                    zf.write(file_path, arcname)
                except:
                    pass
                    
    return send_file(zip_path, as_attachment=True, download_name='site_tam_yedek.zip')

@app.route('/admin/galeri/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_galeri_edit(id):
    g = Galeri.query.get_or_404(id)
    if request.method == 'POST':
        g.title = request.form.get('title')
        g.date = request.form.get('date')
        
        from werkzeug.utils import secure_filename
        files = request.files.getlist('images')
        uploaded_count = 0
        for file in files:
            if file and file.filename:
                file_bytes = file.read()
                if file_bytes:
                    filename = secure_filename(file.filename)
                    mime = file.content_type or 'image/jpeg'
                    gr = GaleriResim(
                        galeri_id=id,
                        image_path=f"data/gallery/{filename}",
                        image_data=file_bytes,
                        mimetype=mime
                    )
                    db.session.add(gr)
                    uploaded_count += 1
        db.session.commit()
        if uploaded_count > 0:
            flash(f'{uploaded_count} adet resim başarıyla eklendi.', 'success')
        else:
            flash('Galeri bilgileri başarıyla güncellendi.', 'success')
        return redirect(url_for('admin_galeri_edit', id=id))
    return render_template('admin/galeri_edit.html', galeri=g)

@app.route('/admin/galeri/sil/<int:id>', methods=['POST'])
@login_required
def admin_galeri_sil(id):
    g = Galeri.query.get_or_404(id)
    for resim in g.resimler:
        db.session.delete(resim)
    db.session.delete(g)
    db.session.commit()
    return redirect(url_for('admin_galeri'))


import traceback
from werkzeug.exceptions import HTTPException
@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, HTTPException):
        return e
    return '<pre>' + traceback.format_exc() + '</pre>', 500

# Trigger deployment



@app.route('/iletisim/gonder', methods=['GET', 'POST'], strict_slashes=False)
@app.route('/idareci/iletisim/gonder', methods=['GET', 'POST'], strict_slashes=False)
def iletisim_gonder():
    if request.method == 'GET':
        return redirect('/iletisim.html')
    name = request.form.get('name')
    phone = request.form.get('phone')
    email = request.form.get('email')
    comment = request.form.get('comment')
    if name and email and comment:
        yeni = Mesaj(name=name, phone=phone, email=email, comment=comment)
        db.session.add(yeni)
        db.session.commit()
        return "<script>alert('Mesajınız başarıyla gönderilmiştir. Teşekkür ederiz.'); window.location.href='/iletisim.html';</script>"
    return "<script>alert('Lütfen tüm zorunlu alanları doldurun.'); window.history.back();</script>"

def can_access_mesajlar():
    if session.get('role') == 'admin':
        return True
    if session.get('role') == 'editor':
        ed = EditorUser.query.get(session.get('editor_id'))
        if ed and ed.can_mesaj:
            return True
    return False

@app.route('/admin/mesajlar')
@login_required
def admin_mesajlar():
    if not can_access_mesajlar():
        return redirect(url_for('editor_panel') if session.get('role') == 'editor' else url_for('admin_index'))
    mesajlar = Mesaj.query.order_by(Mesaj.date_added.desc()).all()
    return render_template('admin/mesajlar.html', mesajlar=mesajlar)

@app.route('/admin/mesajlar/sil/<int:id>', methods=['POST'])
@login_required
def admin_mesaj_sil(id):
    if not can_access_mesajlar():
        return redirect(url_for('editor_panel') if session.get('role') == 'editor' else url_for('admin_index'))
    m = Mesaj.query.get_or_404(id)
    db.session.delete(m)
    db.session.commit()
    flash('Mesaj silindi!')
    return redirect(url_for('admin_mesajlar'))

@app.route('/admin/mesajlar/oku/<int:id>', methods=['POST'])
@login_required
def admin_mesaj_oku(id):
    if not can_access_mesajlar():
        return redirect(url_for('editor_panel') if session.get('role') == 'editor' else url_for('admin_index'))
    m = Mesaj.query.get_or_404(id)
    m.is_read = True
    db.session.commit()
    flash('Mesaj okundu olarak işaretlendi.')
    return redirect(url_for('admin_mesajlar'))
