import os
import bs4
from app import app, db, Haber
import update_anasayfa

def regenerate_haber_listesi():
    with app.app_context():
        # Update anasayfa
        try:
            update_anasayfa.update_anasayfa()
        except Exception as e:
            print("Error updating anasayfa:", e)
            
        # Update haber-listesi.html
        if not os.path.exists('haber-listesi.html'):
            return
            
        habers = Haber.query.order_by(Haber.date.desc(), Haber.id.desc()).all()
        
        with open('haber-listesi.html', 'r', encoding='utf-8', errors='ignore') as f:
            soup = bs4.BeautifulSoup(f.read(), 'lxml')
            
        main_div = soup.find('div', class_='col-md-9', id='main')
        if not main_div: return
        
        panel_body = main_div.find('div', class_='panel-body')
        if not panel_body: return
        
        panel_body.clear()
        
        for h in habers:
            img_src = h.image_path if h.image_path else 'data/haber/0.jpg'
            item_html = f'''
            <div class="box">
                <div class="col-md-3">
                    <img src="{img_src}" style="padding-bottom:15px;" width="100%"/>
                </div>
                <div class="col-md-9">
                    <a href="haber/{h.id}-{h.slug}.html" style="font-weight:700;"><h2>{h.title}</h2></a>
                    <a href="haber/{h.id}-{h.slug}.html">Devam...</a>
                </div>
                <div style="clear:both; border-bottom:1px solid #CCC; margin-bottom:15px;"></div>
            </div>
            '''
            panel_body.append(bs4.BeautifulSoup(item_html, 'html.parser'))
            
        with open('haber-listesi.html', 'w', encoding='utf-8') as f:
            f.write(str(soup))
            
def regenerate_haber_html(h):
    with app.app_context():
        import glob
        existing_habers = glob.glob('haber/*.html')
        if not existing_habers:
            return
            
        with open(existing_habers[0], 'r', encoding='utf-8', errors='ignore') as f:
            soup = bs4.BeautifulSoup(f.read(), 'lxml')
            
        main_div = soup.find('div', class_='col-md-9', id='main')
        if not main_div: return
        
        panel_heading = main_div.find('div', class_='panel-heading')
        if panel_heading:
            panel_heading.string = f"Anasayfa  {h.title}"
            
        box = main_div.find('div', class_='box')
        if box:
            box.clear()
            img_src = f"../{h.image_path}" if h.image_path else "../data/haber/0.jpg"
            content_html = f'''
            <div class="col-md-12" style="font-family: 'Oswald', sans-serif; font-weight:700;"><h2>{h.title}</h2></div>
            <div style="clear:both"></div>
            <div class="col-md-9"><img align="left" src="{img_src}" style="padding-bottom:15px;" width="100%"/></div>
            <div class="col-md-3" style="margin-bottom:5px;">
                <div style="float:left; margin-bottom:20px;">
                    <i class="fa fa-print fa-2x"></i><a onclick="window.print()" style="cursor: pointer"><b> kt Al</b></a>
                </div>
            </div>
            <div style="clear:both"></div>
            <div class="col-md-12 text">
                {h.content}
            </div>
            '''
            box.append(bs4.BeautifulSoup(content_html, 'html.parser'))
            
        out_path = os.path.join('haber', f'{h.id}-{h.slug}.html')
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))

if __name__ == '__main__':
    regenerate_haber_listesi()
    print("Regenerated all news and homepage.")
