import glob

for file in glob.glob('*.html'):
    with open(file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    if 'src="/' in content or 'href="/' in content:
        content = content.replace('src="/', 'src="')
        content = content.replace('href="/', 'href="')
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Removed leading slash in {file}')

from app import app, db, Page
with app.app_context():
    pages = Page.query.all()
    for page in pages:
        if page.content:
            page.content = page.content.replace('src="/', 'src="')
            page.content = page.content.replace('href="/', 'href="')
    db.session.commit()
    print('Fixed in database too')
