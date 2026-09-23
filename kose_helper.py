import os
import bs4
from app import db, KoseYazisi, Yazar

def regenerate_single_yazar(yazar_id):
    yazar = Yazar.query.get(yazar_id)
    if not yazar: return
    
    if not os.path.exists('hakkimizda.html'): return
    with open('hakkimizda.html', 'r', encoding='utf-8', errors='ignore') as f:
        base_html = f.read()
        
    soup = bs4.BeautifulSoup(base_html, 'html.parser')
    main_div = soup.find('div', class_='col-md-9')
    if not main_div: return
    
    name = yazar.name
    pic = yazar.image_path if yazar.image_path else 'themes/burokratlar/tema/images/no-image.png'
    
    yazilar = KoseYazisi.query.filter_by(yazar_id=yazar_id).order_by(KoseYazisi.date_added.desc(), KoseYazisi.id.desc()).all()
    
    def get_yazi_link(y):
        d_str = (y.date_added.strftime("%d.%m.%Y") + " - ") if (y.date_added and y.date_added.year > 2000) else ""
        return f'<li><a href="kose-yazilari-{y.id}.html">{d_str}{y.title}</a></li>'

    new_content = bs4.BeautifulSoup(f'''
    <div class="col-md-9" id="main">
        <div class="main">
            <div class="panel panel-primary">
                <div class="panel-heading">Görüş & Politika Notları / {name}</div>
                <div class="panel-body">
                    <div class="col-md-4">
                        <img src="{pic}" style="float: left; max-width: 100%; margin-bottom:10px; margin-right:10px; border-radius: 8px;"/>
                        <br/>
                        <h4><b>{name}</b></h4>
                    </div>
                    <div class="col-md-8">
                        <br/>
                        <h4>Yazarın Yazıları:</h4>
                        <ul>
                            {''.join([get_yazi_link(y) for y in yazilar])}
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>
    ''', 'html.parser')
    
    main_div.replace_with(new_content)
    with open(f'kose-yazar-{yazar_id}.html', 'w', encoding='utf-8') as f:
        f.write(str(soup))


def regenerate_single_kose(k_id):
    yazi = KoseYazisi.query.get(k_id)
    if not yazi: return
    
    if not os.path.exists('hakkimizda.html'): return
    with open('hakkimizda.html', 'r', encoding='utf-8', errors='ignore') as f:
        base_html = f.read()
        
    soup = bs4.BeautifulSoup(base_html, 'html.parser')
    main_div = soup.find('div', class_='col-md-9')
    if not main_div: return
    
    title = yazi.title
    content = yazi.content
    yazar_id = yazi.yazar_id
    yazar = Yazar.query.get(yazar_id)
    
    yazar_name = yazar.name if yazar else "Bilinmeyen Yazar"
    yazar_pic = yazar.image_path if yazar and yazar.image_path else 'themes/burokratlar/tema/images/no-image.png'
    date_prefix = (yazi.date_added.strftime("%d.%m.%Y") + " - ") if (yazi.date_added and yazi.date_added.year > 2000) else ""
    
    new_content = bs4.BeautifulSoup(f'''
    <div class="col-md-9" id="main">
        <div class="main">
            <div class="panel panel-primary">
                <div class="panel-heading">Görüş & Politika Notları / {date_prefix}{title}</div>
                <div class="panel-body">
                    <div class="col-md-12">
                        <div style="float: left; margin-right: 15px; margin-bottom: 15px; text-align: center;">
                            <a href="kose-yazar-{yazar_id}.html">
                                <img src="{yazar_pic}" style="max-width: 150px; border-radius: 8px;"/>
                                <br/><b>{yazar_name}</b>
                            </a>
                        </div>
                        <h3>{date_prefix}{title}</h3>
                        <hr/>
                        <div class="content-text">
                            {content}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    ''', 'html.parser')
    
    main_div.replace_with(new_content)
    with open(f'kose-yazilari-{k_id}.html', 'w', encoding='utf-8') as f:
        f.write(str(soup))
