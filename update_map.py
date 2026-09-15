import re

with open('app.py', 'r', encoding='utf-8') as f:
    text = f.read()

new_func = """def regenerate_temsilcilik_html():
    import json, bs4, os
    from app import Temsilcilik, Page, db
    reps = Temsilcilik.query.order_by(Temsilcilik.city_name).all()
    
    turkey_areas = []
    world_areas = []
    list_html = ""
    
    for rep in reps:
        img_url = f"/{rep.image_path}" if rep.image_path else "/images/default-avatar.png"
        
        custom_data = f"<div style='text-align:center;'><img src='{img_url}' style='width:60px; height:60px; border-radius:50%; object-fit:cover; margin-bottom:5px;'><br><b>{rep.name}</b><br>{rep.phone or ''}</div>"
        
        area_obj = {
            "id": rep.city_code,
            "title": rep.city_name,
            "color": "rgba(0,201,181,0.8)",
            "customData": custom_data
        }
        
        if rep.city_code.startswith('TR-'):
            turkey_areas.append(area_obj)
        else:
            world_areas.append(area_obj)
        
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

    turkey_json = json.dumps(turkey_areas, ensure_ascii=False)
    world_json = json.dumps(world_areas, ensure_ascii=False)
    
    temsil_html = f'''
    <script type="text/javascript" src="/themes/burokratlar/tema/js/ammap.js"></script>
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
    </style>
    <div class="main">
    <div class="panel panel-primary" style="margin-top:20px; border:none;">
    <div class="panel-body">
    <center>
    <h3 style="color:#800000; font-weight:bold; margin-bottom:20px;">Türkiye Temsilcilikleri</h3>
    </center>
    <div id="map" style="width: 100%; height:500px; background:#f9f9f9; border:1px solid #eee; border-radius:10px; margin-bottom: 40px;"></div>
    
    <center>
    <h3 style="color:#800000; font-weight:bold; margin-bottom:20px;">Dünya Temsilcilikleri</h3>
    </center>
    <div id="mapWorld" style="width: 100%; height:500px; background:#f9f9f9; border:1px solid #eee; border-radius:10px;"></div>
    
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
                headings[-1].string = 'İdareci ve Bürokratlar Birliği / Temsilcilikler'
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(str(soup))
                
            slug = 'temsilcilik'
            page = Page.query.filter_by(slug=slug).first()
            if page:
                page.content = str(box) if box else str(panels[-1])
            db.session.commit()
"""

text = re.sub(r'def regenerate_temsilcilik_html\(\):.*?(?=\ndef [a-zA-Z_]+\(|\Z)', new_func, text, flags=re.DOTALL)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(text)
print("Updated regenerate_temsilcilik_html")
