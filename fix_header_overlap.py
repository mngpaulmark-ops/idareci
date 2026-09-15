import os
import glob
import re

html_files = glob.glob(r'C:\Users\turga\OneDrive\Desktop\bürokratlar birliği site yedeği\burokratlarbirligi.org\*.html')

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8', errors='surrogateescape') as f:
        html = f.read()

    # We want to patch the <style> block for slideshoww to force it to crop the left side
    new_style = """
.slideshoww { max-width:50% !important; width:50% !important; left:auto !important; right:0px !important; margin:0 !important; top:-1px; background-color:transparent !important; overflow: hidden !important; }
.slideshoww img {position: absolute; top: 0px; right: 0px !important; left: auto !important; z-index:-999; background-color: transparent !important; }
"""
    # Replace the old style definition
    html = re.sub(
        r'\.slideshoww \{ max-width:100%; left:0px;  margin:0 auto; top:-1px; background-color:#FFF; \}\s*\.slideshoww img \{position: absolute; top: 0px; left: 0px; z-index:-999; max-width:100%; background-color: #eee; \}', 
        new_style.strip(), 
        html
    )
    
    # Also force the logo to be definitely on top
    html = re.sub(
        r'<a href="#" title="[^"]*">\s*<img alt="[^"]*" class="logo img-responsive" src="data/9595428-logo.png" style="margin-top:15px;"',
        r'<a href="#" title="İdareci ve Bürokratlar Birliği Derneği" style="position: relative; z-index: 9999; display: inline-block;"> <img alt="İdareci ve Bürokratlar Birliği Derneği" class="logo img-responsive" src="data/9595428-logo.png" style="margin-top:15px; position: relative; z-index: 9999;"',
        html
    )
    
    with open(filepath, 'w', encoding='utf-8', errors='surrogateescape') as f:
        f.write(html)

print(f"Patched {len(html_files)} HTML files for header layout.")
