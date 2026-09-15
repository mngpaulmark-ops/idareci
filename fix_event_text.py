import re

with open('anasayfa.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    'txt_NextEvents: "Yaklaşan Etkinlikler:"',
    'txt_NextEvents: "Son Etkinlikler:"'
)

# And also "Bu ay için etkinlik bulunamadı" if there are absolutely no events in the database (which isn't the case).
content = content.replace(
    'txt_noEvents: "Bu ay için etkinlik bulunamadı."',
    'txt_noEvents: "Kayıtlı etkinlik bulunamadı."'
)

with open('anasayfa.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("anasayfa.html text updated.")
