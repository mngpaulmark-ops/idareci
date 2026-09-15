import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

safe_update = '''def update_video_html():
    with app.app_context():
        import glob
        videos = Video.query.order_by(Video.order).all()
        if not videos: return
        
        html = ""
        for v in videos:
            html += f"<li><div style='padding: 5px; text-align:center;'>{v.embed_code}<div class='caption' style='margin-top:5px;'><h5 style='font-size:13px; font-weight:bold; color:#333;'>{v.title}</h5></div></div></li>\\n"
            
        for file in glob.glob('anasayfa.html'):
            with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                page = f.read()
            
            import re
            pattern = r'(<div class="panel-body videogaleri jcarousel">.*?<ul>).*?(</ul>\\s*</div>)'
            new_page = re.sub(pattern, r'\\g<1>\\n' + html + r'\\g<2>', page, flags=re.DOTALL)
            
            if new_page != page:
                with open(file, 'w', encoding='utf-8') as f:
                    f.write(new_page)
'''

# Use manual string replacement to avoid regex escape issues
start_idx = content.find('def update_video_html():')
if start_idx != -1:
    end_idx = content.find('def ', start_idx + 10)
    if end_idx == -1: end_idx = len(content)
    
    new_content = content[:start_idx] + safe_update + content[end_idx:]
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Updated update_video_html via string replace.")
else:
    print("Could not find update_video_html")
