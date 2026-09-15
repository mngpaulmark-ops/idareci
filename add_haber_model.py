import re
import os

with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Add Haber model
haber_model = """
class Haber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=True)
    image_path = db.Column(db.String(255), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
"""

if 'class Haber(db.Model):' not in code:
    code = re.sub(r'(class Yonkur\(db\.Model\):.*?date = db\.Column\(db\.DateTime, default=datetime\.utcnow\))', r'\1\n' + haber_model, code, flags=re.DOTALL)
    # also add datetime import if missing
    if 'from datetime import datetime' not in code:
        code = code.replace('from flask_sqlalchemy import SQLAlchemy', 'from flask_sqlalchemy import SQLAlchemy\nfrom datetime import datetime')

# Add Haber routes
haber_routes = """
@app.route('/admin/haber')
def admin_haber():
    habers = Haber.query.order_by(Haber.id.desc()).all()
    return render_template('admin/haber_list.html', habers=habers)

@app.route('/admin/haber/add', methods=['GET', 'POST'])
def admin_haber_add():
    if request.method == 'POST':
        title = request.form.get('title')
        slug = secure_filename(title.lower().replace(' ', '-').replace('ı', 'i').replace('ğ', 'g').replace('ü', 'u').replace('ş', 's').replace('ö', 'o').replace('ç', 'c'))
        content = request.form.get('content')
        
        file = request.files.get('file')
        image_path = None
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_path = 'data/uploads/' + filename
            
        new_haber = Haber(title=title, slug=slug, content=content, image_path=image_path)
        db.session.add(new_haber)
        db.session.commit()
        
        regenerate_haber_html(new_haber)
        return redirect(url_for('admin_haber'))
    return render_template('admin/haber_edit.html', haber=None)

@app.route('/admin/haber/edit/<int:id>', methods=['GET', 'POST'])
def admin_haber_edit(id):
    haber = Haber.query.get_or_404(id)
    if request.method == 'POST':
        haber.title = request.form.get('title')
        haber.content = request.form.get('content')
        
        file = request.files.get('file')
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            haber.image_path = 'data/uploads/' + filename
            
        db.session.commit()
        regenerate_haber_html(haber)
        return redirect(url_for('admin_haber'))
    return render_template('admin/haber_edit.html', haber=haber)

@app.route('/admin/haber/delete/<int:id>', methods=['POST'])
def admin_haber_delete(id):
    haber = Haber.query.get_or_404(id)
    # Try to delete the html file
    html_path = f"haber/{haber.id}-{haber.slug}.html"
    if os.path.exists(html_path):
        try:
            os.remove(html_path)
        except:
            pass
    db.session.delete(haber)
    db.session.commit()
    return redirect(url_for('admin_haber'))

def regenerate_haber_html(haber):
    # This will read a template and write a static HTML file
    import bs4
    
    html_path = f"haber/{haber.id}-{haber.slug}.html"
    
    # We will use an existing news file as template, e.g. haber/1-burokratlar-birligi-adanada.html
    # But wait, we need to make sure the template exists.
    template_path = 'haber/1-burokratlar-birligi-adanada.html'
    if not os.path.exists(template_path):
        print("Template not found!")
        return
        
    with open(template_path, 'r', encoding='utf-8', errors='ignore') as f:
        soup = bs4.BeautifulSoup(f.read(), 'lxml')
        
    # Find the title box
    h2 = soup.find('h2')
    if h2:
        h2.string = haber.title
        
    # Find content box
    content_div = soup.find('div', class_='content')
    if not content_div:
        # Fallback to looking for panel-body
        panels = soup.find_all('div', class_='panel-body')
        if panels:
            content_div = panels[-1]
            
    if content_div:
        # We need to construct new content
        new_content = ""
        if haber.image_path:
            new_content += f'<center><img src="/{haber.image_path}" style="max-width:100%; border-radius:8px; margin-bottom:20px;"></center>'
        new_content += haber.content
        
        # Clear existing paragraphs or content inside the box that is not the title
        # Actually it's safer to just replace the inner HTML of the specific box
        # Let's find the 'box' inside panel-body
        box = content_div.find('div', class_='box')
        if box:
            box.clear()
            box.append(bs4.BeautifulSoup(new_content, 'html.parser'))
        else:
            # Maybe just append to panel-body?
            pass
            
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
"""

if 'def admin_haber():' not in code:
    code = code + '\n' + haber_routes

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)
print("Updated app.py with Haber routes")
