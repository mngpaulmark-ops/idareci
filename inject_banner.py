import re

for filename in ['generate_kose.py', 'app_kose.py']:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            c = f.read()
            
        old_template = """<hr/>
                            <div class="content-text">
                                {content}
                            </div>"""
                            
        new_template = """<hr/>
                            {'''<img src="themes/burokratlar/tema/images/yucel_can_banner.jpg" style="width:100%; max-width:100%; border-radius:8px; margin-bottom:20px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);"/><br/>''' if str(yazar_id) == '1' else ''}
                            <div class="content-text">
                                {content}
                            </div>"""
                            
        if old_template in c:
            c = c.replace(old_template, new_template)
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(c)
    except:
        pass

print("Updated generators with banner.")
