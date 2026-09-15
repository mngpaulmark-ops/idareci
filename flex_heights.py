import re

with open('anasayfa.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Make `.news` a flex container and stretch children
content = content.replace('<div class="news">', '<div class="news" style="display: flex; flex-wrap: wrap; align-items: stretch;">')

# Make the columns stretch
content = content.replace('<div class="panel-body col-md-6">', '<div class="panel-body col-md-6" style="display: flex; flex-direction: column;">')

# Make the panels stretch to fill the column
# Careful: there are multiple .panel.panel-primary in the document.
# I will specifically target the ones inside the news block.
# Actually, I'll just use a small scoped CSS style block.

css_fix = """
<style>
.news { display: flex; flex-wrap: wrap; align-items: stretch; }
.news > .col-md-6 { display: flex; flex-direction: column; }
.news > .col-md-6 > .pr15 { display: flex; flex-direction: column; flex: 1; }
.news .panel.panel-primary { display: flex; flex-direction: column; flex: 1; margin-bottom: 0; height: 100%; }
.news .panel.panel-primary > .panel-body { flex: 1; display: flex; flex-direction: column; }
#trt-widget { flex: 1; height: auto !important; min-height: 332px; }
</style>
"""

if '.news > .col-md-6' not in content:
    content = content.replace('<div class="news">', css_fix + '\n<div class="news">')
    
    # Also I need to remove the inline style from the Python script I just ran to avoid conflict, but it's fine since flex takes over.
    with open('anasayfa.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Flexbox CSS added successfully.")
else:
    print("Flexbox CSS already exists.")
