import os
import glob
import re

html_files = glob.glob(r'C:\Users\turga\OneDrive\Desktop\bürokratlar birliği site yedeği\burokratlarbirligi.org\*.html')

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8', errors='surrogateescape') as f:
        html = f.read()

    # Update the CSS again to enforce the image doesn't shrink
    old_style = ".slideshoww img {position: absolute; top: 0px; right: 0px !important; left: auto !important; z-index:-999; background-color: transparent !important; }"
    new_style = ".slideshoww img {position: absolute; top: 0px; right: 0px !important; left: auto !important; z-index:-999; background-color: transparent !important; max-width: none !important; width: 1140px !important; height: 155px !important; }"
    
    if old_style in html:
        html = html.replace(old_style, new_style)
        with open(filepath, 'w', encoding='utf-8', errors='surrogateescape') as f:
            f.write(html)

print(f"Patched HTML files for slideshow image size.")
