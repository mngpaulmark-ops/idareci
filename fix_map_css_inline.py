import re

with open('update_map.py', 'r', encoding='utf-8') as f:
    code = f.read()

pattern = re.compile(r'<style>\s*\.amcharts-balloon-div \{ z-index: 9999 !important; padding:10px !important; \}\s*</style>')
replacement = """<style>
        .amcharts-balloon-div { z-index: 9999 !important; padding:10px !important; }
        @media (max-width: 768px) {
            #map, #mapWorld { height: 280px !important; width: 100% !important; margin: 0 auto !important; }
        }
    </style>"""

new_code = re.sub(pattern, replacement, code)

with open('update_map.py', 'w', encoding='utf-8') as f:
    f.write(new_code)
