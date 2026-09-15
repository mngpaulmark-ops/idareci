import glob

for file in glob.glob('*.html'):
    with open(file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Check if slideshoww exists
    if 'class="slideshoww" style="position:absolute; z-index:-99;"' in content:
        content = content.replace(
            'class="slideshoww" style="position:absolute; z-index:-99;"',
            'class="slideshoww" style="position:absolute; z-index:-99; right:0;"'
        )
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Updated {file}')

from app import app, db, Page
with app.app_context():
    pages = Page.query.all()
    for page in pages:
        if page.content and 'class="slideshoww" style="position:absolute; z-index:-99;"' in page.content:
            page.content = page.content.replace(
                'class="slideshoww" style="position:absolute; z-index:-99;"',
                'class="slideshoww" style="position:absolute; z-index:-99; right:0;"'
            )
    db.session.commit()
    print('Updated DB')
