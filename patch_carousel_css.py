import re
import os

path = os.path.join(r'C:\Users\turga\OneDrive\Desktop\bürokratlar birliği site yedeği\burokratlarbirligi.org', 'anasayfa.html')
with open(path, 'r', encoding='utf-8', errors='surrogateescape') as f:
    html = f.read()

css_patch = """
<style>
/* Override jCarousel default styles to enforce uniform image dimensions and alignment */
.fotogaleri.jcarousel img, 
.videogaleri.jcarousel img {
    width: 90% !important;
    height: 140px !important;
    object-fit: cover !important;
    border-radius: 8px !important;
    margin: 0 auto !important;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
}

.fotogaleri.jcarousel .caption, 
.videogaleri.jcarousel .caption {
    text-align: center !important;
    margin-top: 10px !important;
    height: 50px !important;
    overflow: hidden !important;
    font-size: 13px !important;
    line-height: 1.2 !important;
}

.fotogaleri.jcarousel li,
.videogaleri.jcarousel li {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: flex-start !important;
}

.center-image {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    width: 100% !important;
    text-decoration: none !important;
}

.center-image h5 {
    font-size: 13px !important;
    color: #555 !important;
    margin: 5px 0 0 0 !important;
    padding: 0 5px !important;
}
</style>
"""

if "/* Override jCarousel default styles" not in html:
    # Inject right before </head>
    html = html.replace("</head>", css_patch + "</head>")
    
with open(path, 'w', encoding='utf-8', errors='surrogateescape') as f:
    f.write(html)
    
print("Injected CSS patch into anasayfa.html")
