from app import app, db, Galeri
with app.app_context():
    db.session.add(Galeri(title='TEST GALERI GEMINI'))
    db.session.commit()
    print('Added!')
