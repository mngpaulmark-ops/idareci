import os, re, glob

for file in glob.glob('*.html') + glob.glob('haber/*.html'):
    if not os.path.isfile(file): continue
    try:
        with open(file, 'r', encoding='utf-8') as f:
            c = f.read()
    except: continue
        
    original_c = c
    
    # Remove margin-bottom from side-banner
    c = re.sub(r'(class="side-banner"[^>]*?)margin-bottom:\s*20px;?', r'\1margin-bottom: 0px;', c)

    # Remove margin-top from hadis-i-serif
    c = re.sub(r'(class="panel panel-primary hadis-i-serif"[^>]*?)margin-top:\s*20px;?', r'\1margin-top: 0px;', c)
    
    if c != original_c:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(c)

print("Removed margins from all HTML files")
