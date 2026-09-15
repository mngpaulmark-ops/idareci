import os
import re

def regenerate_resimler_html():
    from app import app, Galeri
    with app.app_context():
        galeriler = Galeri.query.order_by(Galeri.id.desc()).all()
        
        blocks = []
        for g in galeriler:
            cover_img = "themes/burokratlar/tema/images/no-image.png"
            if g.resimler and len(g.resimler) > 0:
                cover_img = g.resimler[0].image_path
                
            date_str = g.date or ""
            loc_str = g.location or ""
            title_str = g.title or ""
            
            block = f'''  <div class="col-md-4 mb-4" style="margin-bottom:20px; text-align:center;">
    <div class="card" style="border: 1px solid #e0e0e0; border-radius: 8px; overflow: hidden; padding: 10px; background: #fff;">
        <a href="galeri-resimler-{g.id}.html" style="text-decoration:none;">
            <img class="img-responsive rounded shadow" onerror="this.src='themes/burokratlar/tema/images/no-image.png'" src="{cover_img}" style="width:100%; height:200px !important; object-fit:cover !important; border-radius:8px;"/>
        </a>
        <div style="display: flex; justify-content: space-between; font-size: 12px; color: #888; margin-top: 10px; padding: 0 5px;">
            <span><i class="fa fa-calendar" style="color: #c00;"></i> {date_str}</span>
            <span><i class="fa fa-map-marker" style="color: #c00;"></i> {loc_str}</span>
        </div>
        <div style="text-align: center; margin-top: 10px; min-height: 45px;">
            <a href="galeri-resimler-{g.id}.html" style="color: #1a7bb9; text-decoration: none; font-size: 14px;">{title_str}</a>
        </div>
    </div>
  </div>'''
            blocks.append(block)
            
        full_html = "\n".join(blocks)
        
        path = os.path.join(r'C:\\Users\\turga\\OneDrive\\Desktop\\bürokratlar birliği site yedeği\\burokratlarbirligi.org', 'resimler.html')
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                page = f.read()
                
            # Replace inside the panel-body row
            pattern = r'(<div class="panel-body">\s*<div class="row">).*?(</div>\s*</div>\s*</div>)'
            new_page = re.sub(pattern, r'\g<1>\n' + full_html.replace('\\', '\\\\') + r'\n\g<2>', page, flags=re.DOTALL)
            
            if new_page != page:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_page)
