with open('app.py', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace(
    'img_url = f"/{rep.image_path}" if rep.image_path else "/images/default-avatar.png"', 
    'img_url = rep.image_path if rep.image_path else "themes/burokratlar/tema/images/icon-member.png"'
)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(c)

print("Updated image path logic in app.py")
