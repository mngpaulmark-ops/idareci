with open('update_map.py', 'r', encoding='utf-8') as f:
    code = f.read()

old = """<style>
        .amcharts-balloon-div { z-index: 9999 !important; padding:10px !important; }
    </style>"""
    
# In the script it's represented as double curly braces because of f-string formatting!
old_actual = """<style>
        .amcharts-balloon-div {{ z-index: 9999 !important; padding:10px !important; }}
    </style>"""

new_style = """<style>
        .amcharts-balloon-div {{ z-index: 9999 !important; padding:10px !important; }}
        .ammap-container {{ width: 100%; height: 500px; }}
        @media (max-width: 768px) {{
            .ammap-container {{ height: 300px !important; margin: 0 auto !important; }}
        }}
    </style>"""

code = code.replace(old_actual, new_style)

with open('update_map.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Fixed <style> block in update_map.py!")
