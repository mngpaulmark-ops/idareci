import bs4
import glob

# HTML for the new widget to replace the Facebook block
new_widget_html = '''
<div class="panel panel-sto panel-primary" id="akademik-paneller">
    <div class="panel-heading">
        <i class="glyphicon glyphicon-education" style="font-size: 16px; margin-right: 8px;"></i> Akademik Paneller & Seminerler
    </div>
    <div class="panel-body" style="padding: 15px;">
        <div style="background-color: #f9f9f9; border-left: 4px solid #2980b9; padding: 12px; margin-bottom: 15px; border-radius: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
            <h4 style="color: #2980b9; font-weight: bold; margin-top: 0; font-size: 15px;">Kamu Etiği ve Yönetim İlkeleri</h4>
            <p style="font-size: 13px; color: #555; margin-bottom: 8px;">Kamuda etik değerler ve şeffaf yönetim anlayışı üzerine düzenlenen güncel seminer programlarımız.</p>
            <a href="#" class="btn btn-primary btn-xs" style="background-color: #2980b9; border:none;">Detayları İncele <i class="glyphicon glyphicon-chevron-right"></i></a>
        </div>
        
        <div style="background-color: #f9f9f9; border-left: 4px solid #e74c3c; padding: 12px; border-radius: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
            <h4 style="color: #e74c3c; font-weight: bold; margin-top: 0; font-size: 15px;">Yönetim ve Liderlik Seminerleri</h4>
            <p style="font-size: 13px; color: #555; margin-bottom: 8px;">Geleceğin yöneticilerini yetiştiren vizyoner liderlik eğitimleri ve akademik panel serileri.</p>
            <a href="#" class="btn btn-danger btn-xs" style="background-color: #e74c3c; border:none;">Seminerlere Git <i class="glyphicon glyphicon-chevron-right"></i></a>
        </div>
    </div>
</div>
'''

new_soup = bs4.BeautifulSoup(new_widget_html, 'html.parser')

for file in glob.glob('anasayfa.html'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    soup = bs4.BeautifulSoup(content, 'lxml')
    
    # Find the Sosyal Medya panel
    # It has the class panel-light-red and contains "Sosyal Medya" in heading
    panels = soup.find_all('div', class_='panel-sto')
    for panel in panels:
        heading = panel.find('div', class_='panel-heading')
        if heading and 'Sosyal Medya' in heading.get_text():
            # Replace the entire panel with our new widget
            panel.replace_with(new_soup)
            print(f"Replaced Sosyal Medya panel in {file}")
            break
            
    with open(file, 'w', encoding='utf-8') as f:
        f.write(str(soup))
