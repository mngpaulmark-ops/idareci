import app
import bs4
import glob

with app.app.app_context():
    blocks = {b.slug: b.is_active for b in app.SidebarBlock.query.all()}
    print(f"Blocks: {blocks}")
    
    for file in ['anasayfa.html']:
        with open(file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        soup = bs4.BeautifulSoup(content, 'lxml')
        
        dijital = soup.find('div', class_='side-dijital')
        if dijital:
            print(f"Found dijital: {dijital.get('class')}")
            is_active = blocks.get('dijital', True)
            app._toggle_display(dijital, is_active)
            print(f"After toggle, style is: {dijital.get('style')}")
            
        with open(file, 'w', encoding='utf-8') as f:
            f.write(str(soup))
