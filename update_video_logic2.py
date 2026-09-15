import re

with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

safe_update = """def update_video_html():
    with app.app_context():
        import glob, bs4, re
        videos = Video.query.order_by(Video.order).all()
        
        # 1. Update anasayfa.html
        html = ""
        for v in videos:
            html += f"<li><div style='padding: 5px; text-align:center;'>{v.embed_code}<div class='caption' style='margin-top:5px;'><h5 style='font-size:13px; font-weight:bold; color:#333;'>{v.title}</h5></div></div></li>\\n"
        for file in glob.glob('anasayfa.html'):
            with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                page = f.read()
            pattern = r'(<div class="panel-body videogaleri jcarousel">\\s*<ul>).*?(</ul>\\s*</div>)'
            new_page = re.sub(pattern, r'\\g<1>\\n' + html + r'\\g<2>', page, flags=re.DOTALL)
            if new_page != page:
                with open(file, 'w', encoding='utf-8') as f:
                    f.write(new_page)
                    
        # 2. Update videolar.html
        videolar_html = ""
        if not videos:
            # Fallback to old dummy video blocks if database is empty
            for i in range(1, 5):
                videolar_html += f'''<div class="col-md-6 mb-4" style="margin-bottom:20px;">
                <div class="gallery-hover shadow" style="background:#000; height:200px; display:flex; align-items:center; justify-content:center; color:white; font-size:40px; border-radius:8px; cursor:pointer;">
                ►
                </div>
                <h4 class="text-center mt-2" style="text-align:center;">Video {i}</h4>
                </div>\\n'''
        else:
            for v in videos:
                videolar_html += f'''<div class="col-md-6 mb-4" style="margin-bottom:20px;">
                    <div class="shadow" style="border-radius:8px; overflow:hidden;">
                        {v.embed_code}
                    </div>
                    <h4 class="text-center mt-2" style="text-align:center;">{v.title}</h4>
                </div>\\n'''
                
        for file in glob.glob('videolar.html'):
            with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                page2 = f.read()
            soup = bs4.BeautifulSoup(page2, 'html.parser')
            main_div = soup.find('div', id='main')
            if main_div:
                panel_body = main_div.find('div', class_='panel-body')
                if panel_body:
                    row_div = panel_body.find('div', class_='row')
                    if row_div:
                        row_div.clear()
                        row_div.append(bs4.BeautifulSoup(videolar_html, 'html.parser'))
                        with open(file, 'w', encoding='utf-8') as f:
                            f.write(str(soup))
"""

start_idx = code.find('def update_video_html():')
if start_idx != -1:
    end_idx = code.find('if __name__ == ', start_idx)
    if end_idx == -1: end_idx = len(code)
    
    new_code = code[:start_idx] + safe_update + "\n\n" + code[end_idx:]
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(new_code)
    print("Updated update_video_html to handle fallback dummy videos")
else:
    print("Could not find update_video_html")
