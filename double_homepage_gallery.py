import re

with open('anasayfa.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# CSS to make homepage photo and video galleries 2x taller
css_inject = """
<style>
.photo-gallery .fotogaleri img, .video-gallery .videogaleri img {
    height: 250px !important; /* Doubled height for carousel images */
    width: 100% !important;
    object-fit: cover !important;
}
.photo-gallery .fotogaleri li, .video-gallery .videogaleri li {
    width: 350px !important; /* Make them wider to maintain aspect ratio with new height */
}
</style>
"""

if '.photo-gallery .fotogaleri img' not in content:
    content = content.replace('</head>', css_inject + '\n</head>')
    with open('anasayfa.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Homepage gallery height doubled via CSS!")
else:
    print("CSS already injected.")
