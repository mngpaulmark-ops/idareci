with open('anasayfa.html', 'r', encoding='utf-8') as f:
    c = f.read()
c = c.replace('id="panel-kamu-etigi"', 'id="panel-kamu-etigi" style=""')
c = c.replace('id="panel-yonetim-liderlik"', 'id="panel-yonetim-liderlik" style=""')
with open('anasayfa.html', 'w', encoding='utf-8') as f:
    f.write(c)
