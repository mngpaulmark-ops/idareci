with open('anasayfa.html', 'r', encoding='utf-8', errors='ignore') as f:
    c = f.read()

c = c.replace(
    '<div class="panel panel-sto panel-primary" id="panel-kamu-etigi">',
    '<div class="panel panel-sto panel-primary" id="panel-kamu-etigi" style="">'
)
c = c.replace(
    '<div class="panel panel-sto panel-primary" id="panel-yonetim-liderlik">',
    '<div class="panel panel-sto panel-primary" id="panel-yonetim-liderlik" style="">'
)

with open('anasayfa.html', 'w', encoding='utf-8') as f:
    f.write(c)
