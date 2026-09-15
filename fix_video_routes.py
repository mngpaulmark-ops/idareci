import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

admin_route = '''
@app.route('/admin/videos', methods=['GET', 'POST'])
@login_required
def admin_videos():
    if request.method == 'POST':
        title = request.form.get('title')
        embed = request.form.get('embed_code')
        order = request.form.get('order', type=int, default=0)
        db.session.add(Video(title=title, embed_code=embed, order=order))
        db.session.commit()
        
        import threading
        threading.Thread(target=update_video_html).start()
        
        from flask import flash, redirect, url_for
        flash('Video başarıyla eklendi.', 'success')
        return redirect(url_for('admin_videos'))
        
    videos = Video.query.order_by(Video.order).all()
    return render_template('admin/video_list.html', videos=videos)

@app.route('/admin/videos/delete/<int:id>', methods=['POST'])
@login_required
def admin_video_delete(id):
    v = Video.query.get_or_404(id)
    db.session.delete(v)
    db.session.commit()
    import threading
    threading.Thread(target=update_video_html).start()
    from flask import flash, redirect, url_for
    flash('Video başarıyla silindi.', 'success')
    return redirect(url_for('admin_videos'))

def update_video_html():
    with app.app_context():
        import bs4, glob
        videos = Video.query.order_by(Video.order).all()
        if not videos: return
        
        html = ""
        for v in videos:
            html += f"<li><div style='padding: 5px; text-align:center;'>{v.embed_code}<div class='caption' style='margin-top:5px;'><h5 style='font-size:13px; font-weight:bold; color:#333;'>{v.title}</h5></div></div></li>\\n"
            
        for file in glob.glob('anasayfa.html'):
            with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            soup = bs4.BeautifulSoup(content, 'lxml')
            
            vg = soup.find('div', class_='videogaleri')
            if vg:
                ul = vg.find('ul')
                if ul:
                    new_ul = bs4.BeautifulSoup(f"<ul>\\n{html}</ul>", 'html.parser')
                    ul.replace_with(new_ul)
                    with open(file, 'w', encoding='utf-8') as f:
                        f.write(str(soup))
'''

if 'def admin_videos():' not in content:
    content = content.replace("@app.route('/admin/sidebar'", admin_route + "\n@app.route('/admin/sidebar'")

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Added Video routes to app.py")
