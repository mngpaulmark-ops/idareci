from app import app, db, SidebarBlock, update_sidebar_html
import re

with app.app_context():
    b = SidebarBlock.query.filter_by(slug='hadis').first()
    print('Before DB:', b.is_active)
    
    # Just to test regex replace without saving to DB
    c = open('anasayfa.html', 'r', encoding='utf-8').read()
    
    class_name = 'hadis-i-serif'
    pattern = r'(<div[^>]*class="[^"]*' + re.escape(class_name) + r'[^"]*"[^>]*style=")([^"]*)(")'
    
    def replacer(match):
        return match.group(1) + " TESTING_REPLACE " + match.group(3)
        
    new_c, num = re.subn(pattern, replacer, c)
    print("Replaced:", num)
    if num > 0:
        match = re.search(r'<div[^>]*class="[^"]*' + re.escape(class_name) + r'[^"]*"[^>]*style="([^"]*)"', new_c)
        if match:
            print("New style:", match.group(1))

