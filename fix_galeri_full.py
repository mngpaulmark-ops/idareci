from app import app, db, Galeri, GaleriResim
from galeri_helper import regenerate_resimler_html

initial_galleries = [
    {"date": "16 Haziran 2016", "location": "Ankara", "title": "2016 Yılı Geleneksel İftar Programı", "img": "data/gallery/2049.jpg"},
    {"date": "18 Aralık 2017", "location": "Ankara", "title": "Anadolu Meydanı KUDÜS Mitingi / Ankara / Aralık 2017", "img": "data/gallery/2141.jpg"},
    {"date": "06 Haziran 2018", "location": "Ankara", "title": "Kardeşlik Sınır Tanımaz Projesi / Ankara / Haziran 2018", "img": "data/gallery/2153.jpg"},
    {"date": "23 Kasım 2017", "location": "Ankara", "title": "Kardeşlik Sınır Tanımaz Projesi / Ankara / Kasım 2017", "img": "data/gallery/2113.jpg"},
    {"date": "19 Ağustos 2017", "location": "Hakkari", "title": "Kardeşlik Sınır Tanımaz Projesi / Hakkari / Ağustos 2017", "img": "data/gallery/2091.jpg"},
    {"date": "16 Haziran 2016", "location": "Ankara", "title": "Kardeşlik, Birlik ve Beraberlik Yardım Kampanyası", "img": "data/gallery/2079.jpg"},
    {"date": "", "location": "", "title": "Yetim Türkmen Çocuklarına Yardım Kampanyası", "img": "data/gallery/2102.jpg"}
]

with app.app_context():
    # Delete all
    GaleriResim.query.delete()
    Galeri.query.delete()
    db.session.commit()
    
    # Re-add
    for gdata in initial_galleries:
        g = Galeri(title=gdata["title"], date=gdata["date"], location=gdata["location"])
        db.session.add(g)
        db.session.flush() # get id
        gr = GaleriResim(galeri_id=g.id, image_path=gdata["img"])
        db.session.add(gr)
        
    db.session.commit()
    
    # Regenerate
    regenerate_resimler_html()
    print("Fixed galeri DB and regenerated resimler.html")
