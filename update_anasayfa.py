import os
import bs4
from app import app, db, Haber, Duyuru

def update_anasayfa():
    with app.app_context():
        # Get latest 10 news
        latest = Haber.query.order_by(Haber.date.desc(), Haber.id.desc()).limit(10).all()
        
        # DUYURULAR GÜNCELLEME
        duyurular_db = Duyuru.query.order_by(Duyuru.date_added.desc(), Duyuru.id.desc()).limit(10).all()
        
        duyuru_html = ""
        for d in duyurular_db:
            link = d.link if d.link else "#"
            duyuru_html += f'<li class="news-item"><a href="{link}">{d.title}</a></li>\n'
            
        if not duyuru_html:
            duyuru_html = '<li class="news-item"><a href="#">İdareci ve Bürokratlar Birliği Derneği Web Sitesine Hoşgeldiniz...</a></li>'

        for file in ['anasayfa.html', 'index.html']:
            if os.path.exists(file):
                with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                    soup = bs4.BeautifulSoup(f.read(), 'lxml')
                    
                # Update duyurular
                duyuru_ul = soup.find('ul', id='duyurular')
                if duyuru_ul:
                    duyuru_ul.clear()
                    duyuru_ul.append(bs4.BeautifulSoup(duyuru_html, 'html.parser'))
                
            # Update slider: <ul class="slideshow">
            slider = soup.find('ul', class_='slideshow')
            if slider:
                slider.clear()
                for h in latest:
                    img_src = h.image_path if h.image_path else 'data/haber/0.jpg'
                    li_html = f'''
                    <li>
                        <div class="title">
                            <a href="haber/{h.id}-{h.slug}.html">{h.title}</a>
                        </div>
                        <a href="haber/{h.id}-{h.slug}.html"><img src="{img_src}" alt="{h.title}" /></a>
                    </li>
                    '''
                    slider.append(bs4.BeautifulSoup(li_html, 'html.parser'))
                    
            # Update news list
            news_panel = soup.find('div', class_='news')
            if news_panel:
                list_group = news_panel.find('div', class_='list-group')
                if list_group:
                    list_group.clear()
                    list_group['style'] = "height: 332px; overflow-y: auto; overflow-x: hidden; padding-right: 5px;" 
                    
                    # Remove any extra list-group divs that might be left over from the original template
                    panel_body = news_panel.find('div', class_='col-md-6').find('div', class_='panel-body')
                    if panel_body:
                        extra_groups = panel_body.find_all('div', class_='list-group')
                        for eg in extra_groups[1:]:
                            eg.decompose()
                            
                    for h in latest[:5]: # usually list has 5
                        img_src = h.image_path if h.image_path else 'data/haber/0.jpg'
                        item_html = f'''
                        <div class="col-md-3 list-group-left">
                            <a href="haber/{h.id}-{h.slug}.html"><img src="{img_src}" class="img-responsive"/></a>
                        </div>
                        <div class="col-md-9 list-group-right">
                            <a href="haber/{h.id}-{h.slug}.html">{h.title}</a>
                        </div>
                        <div class="clearfix"></div>
                        '''
                        list_group.append(bs4.BeautifulSoup(item_html, 'html.parser'))
            
            with open(file, 'w', encoding='utf-8') as f:
                f.write(str(soup))
        
        print("Updated anasayfa.html and index.html")

if __name__ == '__main__':
    update_anasayfa()
