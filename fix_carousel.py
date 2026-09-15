import re

with open('themes/burokratlar/tema/css/style.css', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the img { max-width: 100%; height: auto; } block
pattern = r'img\s*\{\s*max-width:\s*100%;\s*height:\s*auto;\s*\}'
content = re.sub(pattern, '', content)

with open('themes/burokratlar/tema/css/style.css', 'w', encoding='utf-8') as f:
    f.write(content)

print("Removed global img responsive css to fix jCarousel.")
