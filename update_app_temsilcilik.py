import os

# 1. Update app.py
with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Insert Temsilcilik Model before # ================= MODELLER ================= ends or before db.create_all()
if 'class Temsilcilik(db.Model):' not in code:
    model_code = """
class Temsilcilik(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city_code = db.Column(db.String(10), nullable=False)
    city_name = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(50), nullable=True)
    image_path = db.Column(db.String(200), nullable=True)
    order = db.Column(db.Integer, default=0)
"""
    # Find a good place to insert (after class Menu)
    code = code.replace('class Menu(db.Model):', model_code + '\nclass Menu(db.Model):')

# 2. Add CITIES dict
cities_code = """
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
    'TR-81': 'Düzce'
}
"""
if 'CITIES = {' not in code:
    code = code.replace('app = Flask(__name__)', 'app = Flask(__name__)\n' + cities_code)

# 3. Add regenerate_temsilcilik_html function
temsilcilik_regen_code = """
def regenerate_temsilcilik_html():
    import json, bs4, os
    reps = Temsilcilik.query.order_by(Temsilcilik.city_name).all()
    areas = []
    list_html = ""
    
    for rep in reps:
        img_url = f"/{rep.image_path}" if rep.image_path else "/images/default-avatar.png"
        
        # HTML for map balloon
        custom_data = f"<div style='text-align:center;'><img src='{img_url}' style='width:60px; height:60px; border-radius:50%; object-fit:cover; margin-bottom:5px;'><br><b>{rep.name}</b><br>{rep.phone or ''}</div>"
        
        areas.append({
            "id": rep.city_code,
            "title": rep.city_name,
            "color": "rgba(0,201,181,0.8)",
            "customData": custom_data
        })
        
        list_html += f'''
        <div class="col-12 col-md-6 col-lg-4" style="margin-bottom:20px; display:flex;">
            <div class="card border-0 shadow-sm" style="background:#fff; border-radius:10px; padding:15px; display:flex; flex-direction:row; align-items:center; width:100%; border: 1px solid #f1f1f1;">
                <img src="{img_url}" style="width:70px; height:70px; border-radius:50%; object-fit:cover; margin-right:15px; border:2px solid #eaeaea;" onerror="this.src='/images/default-avatar.png'; this.onerror=null;">
                <div>
                    <h5 style="color:#800000; font-size:16px; font-weight:700; margin-bottom:5px;">{rep.name}</h5>
                    <div style="font-size:13px; color:#555; font-weight:500;">{rep.city_name} İl Temsilcisi</div>
                    <div style="font-size:13px; color:#777; margin-top:3px;"><i class="fa fa-phone"></i> {rep.phone or ''}</div>
                </div>
            </div>
        </div>
        '''

    areas_json = json.dumps(areas, ensure_ascii=False)
    
    temsil_html = f'''
    <script type="text/javascript" src="/themes/burokratlar/tema/js/ammap.js"></script>
    <script type="text/javascript" src="https://www.amcharts.com/lib/3/maps/js/turkeyLow.js"></script>
    <script type="text/javascript">
            AmCharts.makeChart("map",{{
                    "type": "map",
                    "pathToImages": "http://www.amcharts.com/lib/3/images/",
                    "addClassNames": true,
                    "fontSize": 12,
                    "color": "#000000",
                    "projection": "mercator",
                    "backgroundAlpha": 1,
                    "backgroundColor": "rgba(255,255,255,1)",
                    "dataProvider": {{
                        "map": "turkeyLow",
                        "getAreasFromMap": true,
                        "areas": {areas_json}
                    }},
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
                    "imagesSettings": {{
                        "alpha": 1,
                        "color": "rgba(255,0,0,1)",
                        "outlineAlpha": 0,
                        "rollOverOutlineAlpha": 0,
                        "outlineColor": "rgba(255,255,255,1)",
                        "rollOverBrightness": 20,
                        "selectedBrightness": 20,
                        "selectable": true
                    }},
                    "linesSettings": {{
                        "color": "rgba(255,0,0,1)",
                        "selectable": true,
                        "rollOverBrightness": 20,
                        "selectedBrightness": 20
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
                }});
    </script>
    <style>
        .amcharts-balloon-div {{ z-index: 9999 !important; padding:10px !important; }}
    </style>
    <div class="main">
    <div class="panel panel-primary" style="margin-top:20px; border:none;">
    <div class="panel-body">
    <center>
    <h3 style="color:#800000; font-weight:bold; margin-bottom:20px;">İdareci ve Bürokratlar Birliği İl Temsilcilikleri</h3>
    </center>
    <div id="map" style="width: 100%; height:500px; background:#f9f9f9; border:1px solid #eee; border-radius:10px;"></div>
    
    <div class="row" style="margin-top:40px;">
        {list_html}
    </div>
    
    </div></div><div class="clearfix"></div></div>
    '''
    
    filename = 'temsilcilik.html'
    if os.path.exists('hakkimizda.html'):
        with open('hakkimizda.html', 'r', encoding='utf-8', errors='ignore') as f:
            soup = bs4.BeautifulSoup(f.read(), 'lxml')
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
                headings[-1].string = f'İdareci ve Bürokratlar Birliği / Temsilcilikler'
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(str(soup))
                
            slug = 'temsilcilik'
            page = Page.query.filter_by(slug=slug).first()
            if page:
                page.content = str(box) if box else str(panels[-1])
            db.session.commit()
"""
if 'def regenerate_temsilcilik_html():' not in code:
    code = code.replace('def regenerate_yonkur_html():', temsilcilik_regen_code + '\ndef regenerate_yonkur_html():')

# 4. Remove # 4. Temsilcilik logic from regenerate_yonkur_html
import re
code = re.sub(r"# 4\. Temsilcilik.*?write_to_file_and_db\('temsilcilik.html', temsil_html, 'Temsilcilikler'\)", "", code, flags=re.DOTALL)


# 5. Add routes
admin_temsil_routes = """
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
            rep.image_path = f"uploads/{unique_filename}"
            
        db.session.commit()
        regenerate_temsilcilik_html()
        flash('Temsilcilik güncellendi.')
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
"""
if 'def admin_temsilcilik():' not in code:
    code += '\n' + admin_temsil_routes

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated app.py")
