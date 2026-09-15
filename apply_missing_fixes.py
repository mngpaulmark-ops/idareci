import re
import os

print("Injecting missing visual fixes into HTML...")

# 1. Flex Heights & TRT Widget Sync for anasayfa.html
with open('anasayfa.html', 'r', encoding='utf-8', errors='surrogateescape') as f:
    content = f.read()

js_sync = """
<script>
document.addEventListener("DOMContentLoaded", function() {
    setTimeout(function() {
        var leftPanel = document.querySelector('.news .col-md-6:first-child .panel.panel-primary');
        var trtWidget = document.getElementById('trt-widget');
        var trtPanel = document.querySelector('.news .col-md-6:nth-child(2) .panel.panel-primary');
        
        if (leftPanel && trtWidget && trtPanel) {
            // Match the height of the entire panel
            trtPanel.style.height = leftPanel.offsetHeight + 'px';
            
            // Adjust the inner widget height based on the header height
            var headerHeight = trtPanel.querySelector('.panel-heading').offsetHeight;
            // padding is usually 15px top + 15px bottom for panel-body
            trtWidget.style.height = (leftPanel.offsetHeight - headerHeight - 35) + 'px';
        }
    }, 500); // Wait for images to load
});
</script>
"""

if 'trtPanel.style.height = leftPanel.offsetHeight' not in content:
    content = content.replace('<!-- .panel .panel-primary', js_sync + '\n  <!-- .panel .panel-primary')

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
    
# Remove old slideshow absolute tag if any (from original backup it was missing the absolute right)
# Actually, the user liked the slideshoww (flag/mosque) in header! It's in `anasayfa.html`.
# Let's check if it exists: `<div class="slideshoww">`
if '<div class="slideshoww">' in content:
    content = content.replace('<div class="slideshoww">', '<div class="slideshoww" style="position:absolute; z-index: 1; right:-80px;">')

with open('anasayfa.html', 'w', encoding='utf-8', errors='surrogateescape') as f:
    f.write(content)

# 2. Yanaplat Banner injection for ALL html files
banner_html = '''<div class="side-banner" id="yanaplat-banner" style="margin-top: 20px; margin-bottom: 20px; text-align: center;">
    <img src="data/yanaplat.gif" alt="Milli İrade Platformu" style="width: 100%; height: 220px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); border: 1px solid #ccc;" />
</div>'''

count = 0
for root, dirs, files in os.walk('.'):
    if '.git' in root or '__pycache__' in root or 'venv' in root or 'instance' in root: continue
    for f in files:
        if f.endswith('.html'):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8', errors='surrogateescape') as file:
                html = file.read()
            
            # 1. Remove the old one if it exists
            old_pattern1 = r'<p></p><div style="width:100%; text-align:center;"><img src="data/yanaplat.gif" width="100%"/></div>'
            old_pattern2 = r'<div style="width:100%; text-align:center;"><img src="data/yanaplat.gif" width="100%"/></div>'
            html = html.replace(old_pattern1, '')
            html = html.replace(old_pattern2, '')
            
            # 2. Inject into #left if not already there
            if 'id="yanaplat-banner"' not in html:
                # Find the end of left-menu
                if '</div> <!-- .left-menu -->' in html:
                    html = html.replace('</div> <!-- .left-menu -->', banner_html + '\n</div> <!-- .left-menu -->')
                    with open(path, 'w', encoding='utf-8', errors='surrogateescape') as file:
                        file.write(html)
                    count += 1

print(f"Applied missing visual fixes to {count} files!")
