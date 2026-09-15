import re
with open('app.py', 'r', encoding='utf-8') as f:
    text = f.read()

routes = '''
@app.route('/admin/side_links')
@login_required
def admin_side_links():
    dijital = SideLink.query.filter_by(category='dijital').order_by(SideLink.order).all()
    gundem = SideLink.query.filter_by(category='gundem').order_by(SideLink.order).all()
    ebulten = SideLink.query.filter_by(category='ebulten').first()
    faydali = SideLink.query.filter_by(category='faydali').order_by(SideLink.order).all()
    return render_template('admin/side_links.html', dijital=dijital, gundem=gundem, ebulten=ebulten, faydali=faydali)

@app.route('/admin/side_links/add', methods=['POST'])
@login_required
def admin_side_links_add():
    title = request.form.get('title')
    url = request.form.get('url', '')
    badge = request.form.get('badge', '')
    category = request.form.get('category')
    order = request.form.get('order', type=int)
    
    new_link = SideLink(title=title, url=url, badge=badge, category=category, order=order)
    db.session.add(new_link)
    db.session.commit()
    
    threading.Thread(target=apply_side_links_to_all_html).start()
    return redirect(url_for('admin_side_links'))

@app.route('/admin/side_links/edit/<int:id>', methods=['POST'])
@login_required
def admin_side_links_edit(id):
    link = SideLink.query.get_or_404(id)
    link.title = request.form.get('title')
    link.url = request.form.get('url', '')
    link.badge = request.form.get('badge', '')
    link.order = request.form.get('order', type=int)
    db.session.commit()
    
    threading.Thread(target=apply_side_links_to_all_html).start()
    return redirect(url_for('admin_side_links'))

@app.route('/admin/side_links/delete/<int:id>')
@login_required
def admin_side_links_delete(id):
    link = SideLink.query.get_or_404(id)
    db.session.delete(link)
    db.session.commit()
    threading.Thread(target=apply_side_links_to_all_html).start()
    return redirect(url_for('admin_side_links'))

@app.route('/admin/side_links/toggle/<int:id>')
@login_required
def admin_side_links_toggle(id):
    link = SideLink.query.get_or_404(id)
    link.is_active = not link.is_active
    db.session.commit()
    threading.Thread(target=apply_side_links_to_all_html).start()
    return redirect(url_for('admin_side_links'))
'''

# Find a good place to insert routes
text = text.replace('@app.route(\'/admin/left_menu\')', routes + '\n@app.route(\'/admin/left_menu\')')

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(text)
print('Routes added')
