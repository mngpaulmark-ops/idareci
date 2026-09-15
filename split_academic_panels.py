import bs4
import glob

# HTML for the Left Widget (Kamu Etiği)
left_widget_html = '''
<div class="panel panel-sto panel-primary" id="panel-kamu-etigi">
    <div class="panel-heading" style="background-color: #2980b9;">
        <i class="glyphicon glyphicon-education" style="font-size: 16px; margin-right: 8px;"></i> Kamu Etiği ve Yönetim İlkeleri
    </div>
    <div class="panel-body" style="padding: 15px;">
        <div style="background-color: #f9f9f9; padding: 12px; margin-bottom: 5px; border-radius: 4px;">
            <p style="font-size: 14px; color: #555; margin-bottom: 12px;">Kamuda etik değerler ve şeffaf yönetim anlayışı üzerine düzenlenen güncel seminer programlarımız.</p>
            <a href="#" class="btn btn-primary btn-sm" style="background-color: #2980b9; border:none; width: 100%;">Detayları İncele <i class="glyphicon glyphicon-chevron-right"></i></a>
        </div>
    </div>
</div>
'''

# HTML for the Right Widget (Yönetim ve Liderlik Seminerleri)
right_widget_html = '''
<div class="panel panel-sto panel-danger" id="panel-yonetim-liderlik">
    <div class="panel-heading" style="background-color: #e74c3c; color: white;">
        <i class="glyphicon glyphicon-blackboard" style="font-size: 16px; margin-right: 8px;"></i> Yönetim ve Liderlik Seminerleri
    </div>
    <div class="panel-body" style="padding: 15px;">
        <div style="background-color: #f9f9f9; padding: 12px; border-radius: 4px;">
            <p style="font-size: 14px; color: #555; margin-bottom: 12px;">Geleceğin yöneticilerini yetiştiren vizyoner liderlik eğitimleri ve akademik panel serileri.</p>
            <a href="#" class="btn btn-danger btn-sm" style="background-color: #e74c3c; border:none; width: 100%;">Seminerlere Git <i class="glyphicon glyphicon-chevron-right"></i></a>
        </div>
    </div>
</div>
'''

left_soup = bs4.BeautifulSoup(left_widget_html, 'html.parser')
right_soup = bs4.BeautifulSoup(right_widget_html, 'html.parser')

for file in glob.glob('anasayfa.html'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    soup = bs4.BeautifulSoup(content, 'lxml')
    
    # Replace the current Academic Panels widget with just the left one
    akad_panel = soup.find('div', id='akademik-paneller')
    if akad_panel:
        akad_panel.replace_with(left_soup)
    else:
        print("Could not find akademik-paneller")
        
    # Find the Hava Durumu panel and replace it with the right one
    panels = soup.find_all('div', class_='panel-sto')
    for panel in panels:
        heading = panel.find('div', class_='panel-heading')
        if heading and 'Hava Durumu' in heading.get_text():
            panel.replace_with(right_soup)
            print("Replaced Hava Durumu with Yönetim ve Liderlik widget")
            break
            
    with open(file, 'w', encoding='utf-8') as f:
        f.write(str(soup))
