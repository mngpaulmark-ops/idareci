import re

with open('anasayfa.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Remove the injected style block
# The style block looks like:
# <style>
# .photo-gallery .fotogaleri img, .video-gallery .videogaleri img {
# ...
# </style>

new_content = re.sub(r'<style>\s*\.photo-gallery \.fotogaleri img.*?<\/style>', '', content, flags=re.DOTALL)

with open('anasayfa.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

if new_content != content:
    print("Found and removed the problematic CSS style block from anasayfa.html!")
else:
    print("Could not find the exact style block in anasayfa.html.")
