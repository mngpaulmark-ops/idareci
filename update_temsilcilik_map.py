import sys
with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip = False
for line in lines:
    if line.strip() == "# 4. Temsilcilik":
        skip = True
        
        map_script = """
    # 4. Temsilcilik
    temsil_html = '''
    <script type="text/javascript" src="/themes/burokratlar/tema/js/ammap.js"></script>
    <script type="text/javascript" src="https://www.amcharts.com/lib/3/maps/js/turkeyLow.js"></script>
    <script type="text/javascript">
            AmCharts.makeChart("map",{
                    "type": "map",
                    "pathToImages": "http://www.amcharts.com/lib/3/images/",
                    "addClassNames": true,
                    "fontSize": 12,
                    "color": "#000000",
                    "projection": "mercator",
                    "backgroundAlpha": 1,
                    "backgroundColor": "rgba(255,255,255,1)",
                    "dataProvider": {
                        "map": "turkeyLow",
                        "getAreasFromMap": true,
                        "areas": [
                            { "id": "TR-01", "title": "Adana", "color": "rgba(0,201,181,0.8)" },
                            { "id": "TR-02", "title": "Adıyaman", "color": "rgba(0,201,181,0.8)" },
                            { "id": "TR-04", "title": "Ağrı", "color": "rgba(0,201,181,0.8)" },
                            { "id": "TR-06", "title": "Ankara", "customData" : "Dernek Genel Merkezi", "color": "rgba(0,201,181,0.8)" },
                            { "id": "TR-07", "title": "Antalya", "color": "rgba(0,201,181,0.8)" },
                            { "id": "TR-74", "title": "Bartın", "color": "rgba(0,201,181,0.8)" },
                            { "id": "TR-21", "title": "Diyarbakır", "color": "rgba(0,201,181,0.8)" },
                            { "id": "TR-23", "title": "Elazığ", "color": "rgba(0,201,181,0.8)" },
                            { "id": "TR-26", "title": "Eskişehir", "color": "rgba(0,201,181,0.8)" },
                            { "id": "TR-31", "title": "Hatay", "color": "rgba(0,201,181,0.8)" },
                            { "id": "TR-32", "title": "Isparta", "color": "rgba(0,201,181,0.8)" },
                            { "id": "TR-34", "title": "İstanbul", "color": "rgba(0,201,181,0.8)" },
                            { "id": "TR-46", "title": "Kahramanmaraş", "color": "rgba(0,201,181,0.8)" },
                            { "id": "TR-37", "title": "Kastamonu", "color": "rgba(0,201,181,0.8)" },
                            { "id": "TR-44", "title": "Malatya", "color": "rgba(0,201,181,0.8)" },
                            { "id": "TR-45", "title": "Manisa", "color": "rgba(0,201,181,0.8)" },
                            { "id": "TR-38", "title": "Kayseri", "color": "rgba(0,201,181,0.8)" },
                            { "id": "TR-51", "title": "Niğde", "color": "rgba(0,201,181,0.8)" },
                            { "id": "TR-55", "title": "Samsun", "color": "rgba(0,201,181,0.8)" },
                            { "id": "TR-66", "title": "Yozgat", "color": "rgba(0,201,181,0.75)" }
                        ]
                    },
                    "balloon": {
                        "horizontalPadding": 15,
                        "borderAlpha": 0,
                        "borderThickness": 1,
                        "verticalPadding": 15
                    },
                    "areasSettings": {
                        "color": "rgba(255,0,0,1)",
                        "outlineColor": "rgba(255,255,255,1)",
                        "rollOverOutlineColor": "rgba(255,255,255,1)",
                        "rollOverBrightness": 20,
                        "selectedBrightness": 20,
                        "selectable": true,
                        "unlistedAreasAlpha": 0,
                        "balloonText": "<b>[[title]]</b><br> [[customData]]",
                        "unlistedAreasOutlineAlpha": 0
                    },
                    "imagesSettings": {
                        "alpha": 1,
                        "color": "rgba(255,0,0,1)",
                        "outlineAlpha": 0,
                        "rollOverOutlineAlpha": 0,
                        "outlineColor": "rgba(255,255,255,1)",
                        "rollOverBrightness": 20,
                        "selectedBrightness": 20,
                        "selectable": true
                    },
                    "linesSettings": {
                        "color": "rgba(255,0,0,1)",
                        "selectable": true,
                        "rollOverBrightness": 20,
                        "selectedBrightness": 20
                    },
                    "zoomControl": {
                        "zoomControlEnabled": false,
                        "homeButtonEnabled": false,
                        "panControlEnabled": false,
                        "right": 38,
                        "bottom": 30,
                        "minZoomLevel": 0.25,
                        "gridHeight": 100,
                        "gridAlpha": 0.1,
                        "gridBackgroundAlpha": 0,
                        "gridColor": "#FFFFFF",
                        "draggerAlpha": 1,
                        "buttonCornerRadius": 2
                    }
                });
    </script>
    <div class="main">
    <div class="panel panel-primary" style="margin-top:20px; border:none;">
    <div class="panel-body">
    <center>
    <h3 style="color:#800000; font-weight:bold; margin-bottom:20px;">İdareci ve Bürokratlar Birliği İl Temsilcilikleri</h3>
    </center>
    <div id="map" style="width: 100%; height:500px;"></div>
    
    <div style="margin-top:40px;">
    '''
    
    for member in groups['te']:
        mail = member.get('mail', '')
        name = member.get('name', '')
        unvan = member.get('unvan', '')
        temsil_html += f'''
        <div class="iltemunvan" style="margin-bottom:15px; padding-bottom:15px; border-bottom:1px solid #f3f3f3;">
            <span style="font-size:18px;">
                <a href="mailto:{mail}" target="_blank" style="color:#000; font-weight:bold; text-decoration:none;">{name}</a> / {unvan}
            </span>
        </div>
        '''
        
    temsil_html += '</div></div><div class="clearfix"></div></div></div>'
    write_to_file_and_db('temsilcilik.html', temsil_html, 'Temsilcilikler')
"""
        new_lines.append(map_script)
        continue

    if skip:
        if line.strip() == "write_to_file_and_db('temsilcilik.html', temsil_html, 'Temsilcilik')":
            skip = False
        continue

    new_lines.append(line)

with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Updated app.py with original map template")
