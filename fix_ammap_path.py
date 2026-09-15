import re

with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Fix ammap.js path
code = code.replace('src="/themes/burokratlar/tema/js/ammap.js"', 'src="themes/burokratlar/tema/js/ammap.js"')

# Fix balloon image paths
code = code.replace('img_url = f"/{rep.image_path}" if rep.image_path else "/images/default-avatar.png"', 'img_url = f"{rep.image_path}" if rep.image_path else "images/default-avatar.png"')
code = code.replace('this.src=\'/images/default-avatar.png\'', 'this.src=\'images/default-avatar.png\'')
code = code.replace('src="/images/default-avatar.png"', 'src="images/default-avatar.png"')

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Fixed paths in app.py!")
