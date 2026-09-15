import re

with open('update_map.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Remove the forced zoom parameters
code = code.replace('"zoomLevel": 0.9,', '')
code = code.replace('"zoomLongitude": 35.5,', '')
code = code.replace('"zoomLatitude": 39.0,', '')

# 2. Fix the inline styles to use a class instead
code = code.replace('<div id="map" style="width: 100%; height:500px; background:#f9f9f9; border:1px solid #eee; border-radius:10px; margin-bottom: 40px;"></div>', '<div id="map" class="ammap-container" style="background:#f9f9f9; border:1px solid #eee; border-radius:10px; margin-bottom: 40px;"></div>')
code = code.replace('<div id="mapWorld" style="width: 100%; height:500px; background:#f9f9f9; border:1px solid #eee; border-radius:10px;"></div>', '<div id="mapWorld" class="ammap-container" style="background:#f9f9f9; border:1px solid #eee; border-radius:10px;"></div>')

# 3. Fix the <style> block
old_style = """<style>
        .amcharts-balloon-div { z-index: 9999 !important; padding:10px !important; }
        @media (max-width: 768px) {
            #map, #mapWorld { height: 280px !important; width: 100% !important; margin: 0 auto !important; }
        }
    </style>"""

new_style = """<style>
        .amcharts-balloon-div { z-index: 9999 !important; padding:10px !important; }
        .ammap-container { width: 100%; height: 500px; }
        @media (max-width: 768px) {
            .ammap-container { height: 300px !important; margin: 0 auto !important; }
        }
    </style>"""

code = code.replace(old_style, new_style)

# If it didn't find old_style because it wasn't replaced previously, let's try the original style:
original_style = """<style>
        .amcharts-balloon-div { z-index: 9999 !important; padding:10px !important; }
    </style>"""
code = code.replace(original_style, new_style)

with open('update_map.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Fixed update_map.py using string replace!")
