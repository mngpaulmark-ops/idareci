import re

with open('hakkimizda.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Enhance Colorbox to scale down oversized images to fit the screen
if 'maxWidth:"95%"' not in content:
    content = content.replace(
        "$('a[rel*=fotogaleri]').colorbox();",
        "$('a[rel*=fotogaleri]').colorbox({maxWidth:'95%', maxHeight:'95%', scalePhotos:true});"
    )
    with open('hakkimizda.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Colorbox enhanced in hakkimizda.html")
else:
    print("Colorbox already enhanced.")
