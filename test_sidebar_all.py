from app import app, db, SidebarBlock, update_sidebar_html
import re

with app.app_context():
    c = open('anasayfa.html', 'r', encoding='utf-8').read()
    
    for slug in ['hadis', 'dijital', 'gundem', 'ebulten', 'faydali', 'banner']:
        class_name = 'hadis-i-serif' if slug == 'hadis' else f'side-{slug}'
        pattern = r'(<div[^>]*class="[^"]*' + re.escape(class_name) + r'[^"]*"[^>]*style=")([^"]*)(")'
        new_c, num = re.subn(pattern, r'\g<1>TESTING_REPLACE\g<3>', c)
        print(f"Slug: {slug}, class: {class_name}, Replaced: {num}")

