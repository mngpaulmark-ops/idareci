from app import app, db, Video, update_video_html

with app.app_context():
    if Video.query.count() == 0:
        db.session.add(Video(
            title='Tanıtım Videosu',
            embed_code='<iframe width="100%" height="200" src="https://www.youtube.com/embed/dQw4w9WgXcQ" frameborder="0" allowfullscreen></iframe>'
        ))
        db.session.commit()
    update_video_html()
    print("Populated videos")
