import glob, re

files = glob.glob('*.html') + glob.glob('haber/*.html')
for f in files:
    try:
        content = open(f, encoding='utf-8', errors='ignore').read()
        if 'Mebir.NET' in content or 'mebir.net' in content.lower():
            content = re.sub(r'Tasar[ıi]m.*?Mebir\.NET.*?(</a>|)', '', content, flags=re.IGNORECASE)
            content = content.replace('Mebir.NET', '')
            content = content.replace('mebir.net', '')
            open(f, 'w', encoding='utf-8').write(content)
    except: pass

haber_files = glob.glob('haber/*.html')
for f in haber_files:
    try:
        content = open(f, encoding='utf-8', errors='ignore').read()
        modified = False
        if '<base href=' in content:
            content = re.sub(r'<base href=[^>]+>', '', content)
            modified = True
        if 'fb-root' in content:
            content = content.replace('<div id="fb-root"></div>', '')
            content = re.sub(r'<script[^>]*connect\.facebook\.net[^>]*></script>', '', content)
            modified = True
        
        for url in ['https://burokratlarbirligi.org/', 'http://burokratlarbirligi.org/', 'https://www.burokratlarbirligi.org/', 'http://www.burokratlarbirligi.org/']:
            if url in content:
                content = content.replace(url, '../')
                modified = True
                
        if 'id="dynamic-menu-script"' in content:
            content = re.sub(r'<script id="dynamic-menu-script".*?</script>', '', content, flags=re.DOTALL)
            modified = True
            
        if modified:
            open(f, 'w', encoding='utf-8').write(content)
    except: pass

print('Cleaned haber files and removed Mebir.NET!')
