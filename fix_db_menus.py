import app

with app.app.app_context():
    # Update Gençlik Kolları
    genclik = app.LeftMenu.query.filter_by(title='Gençlik Kolları').first()
    if genclik:
        genclik.url = 'genclik-kollari.html'
        
    # Update Üyelerimiz
    uyeler = app.LeftMenu.query.filter_by(title='Üyelerimiz').first()
    if uyeler:
        uyeler.url = 'uyelik.html'
        
    # Update Haberler
    haberler = app.LeftMenu.query.filter_by(title='Haberler').first()
    if haberler:
        haberler.url = 'haber-listesi.html'
        
    # Update Duyurular
    duyurular = app.LeftMenu.query.filter_by(title='Duyurular').first()
    if duyurular:
        duyurular.url = 'duyurular.html'
        
    # Update Raporlar / Belgeler
    raporlar = app.LeftMenu.query.filter_by(title='Raporlar / Belgeler').first()
    if raporlar:
        raporlar.url = 'raporlar-belgeler.html'
        
    app.db.session.commit()
    
    # Re-apply to all HTML files
    app._apply_menus_inner()

print("Database updated and applied to all HTML files!")
