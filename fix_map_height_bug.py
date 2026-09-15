import re

with open('update_map.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Remove the forced zoom parameters
pattern_zoom = re.compile(r'"zoomLevel": 0\.9,\s*"zoomLongitude": 35\.5,\s*"zoomLatitude": 39\.0,')
code = re.sub(pattern_zoom, '', code)

# 2. Fix the inline styles to use a class instead
pattern_map = re.compile(r'<div id="map" style="width: 100%; height:500px; background:#f9f9f9; border:1px solid #eee; border-radius:10px; margin-bottom: 40px;"></div>')
code = re.sub(pattern_map, '<div id="map" class="ammap-container" style="background:#f9f9f9; border:1px solid #eee; border-radius:10px; margin-bottom: 40px;"></div>', code)

pattern_mapWorld = re.compile(r'<div id="mapWorld" style="width: 100%; height:500px; background:#f9f9f9; border:1px solid #eee; border-radius:10px;"></div>')
code = re.sub(pattern_mapWorld, '<div id="mapWorld" class="ammap-container" style="background:#f9f9f9; border:1px solid #eee; border-radius:10px;"></div>', code)

# 3. Add the class to the <style> block
pattern_style = re.compile(r'<style>.*?@media \(max-width: 768px\) \{.*?\}\s*</style>', re.DOTALL)

new_style = """<style>
        .amcharts-balloon-div { z-index: 9999 !important; padding:10px !important; }
        .ammap-container { width: 100%; height: 500px; }
        @media (max-width: 768px) {
            .ammap-container { height: 300px !important; margin: 0 auto !important; }
        }
    </style>"""

code = re.sub(pattern_style, new_style, code)

with open('update_map.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Fixed update_map.py!")
