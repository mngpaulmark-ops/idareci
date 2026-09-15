import re

files_to_update = ['anasayfa.html', 'hakkimizda.html']

for file in files_to_update:
    try:
        with open(file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        # 1. Remove the old one if it exists
        old_pattern1 = r'<p></p><div style="width:100%; text-align:center;"><img src="data/yanaplat.gif" width="100%"/></div>'
        old_pattern2 = r'<div style="width:100%; text-align:center;"><img src="data/yanaplat.gif" width="100%"/></div>'
        content = content.replace(old_pattern1, '')
        content = content.replace(old_pattern2, '')
        
        # 2. Inject into #left if not already there
        if 'id="yanaplat-banner"' not in content:
            banner_html = '''<div id="yanaplat-banner" style="margin-top: 20px; margin-bottom: 20px; text-align: center;">
    <img src="data/yanaplat.gif" alt="Milli İrade Platformu" style="width: 100%; max-width: 250px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); border: 1px solid #eee;" />
</div>'''
            # Find the end of left-menu
            content = content.replace('</div> <!-- .left-menu -->', banner_html + '\n</div> <!-- .left-menu -->')
            
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"Updated {file}")
    except Exception as e:
        print(f"Error on {file}: {e}")
