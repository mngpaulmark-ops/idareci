import os
import zipfile

zip_path = r'C:\Users\turga\OneDrive\Desktop\burokratlarbirligi_yedek_13.09.2026.zip'
base_dir = r'C:\Users\turga\OneDrive\Desktop\bürokratlar birliği site yedeği\burokratlarbirligi.org'

restored = 0
with zipfile.ZipFile(zip_path, 'r') as z:
    for zf in z.namelist():
        if zf.endswith('.html') and 'templates/' not in zf:
            # zip might have root folder "burokratlarbirligi.org/" or not
            # Let's find the relative path
            parts = zf.split('/')
            if parts[0] == 'burokratlarbirligi.org':
                rel_path = '/'.join(parts[1:])
            else:
                rel_path = zf
                
            if not rel_path: continue
            
            target_path = os.path.join(base_dir, rel_path)
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            
            data = z.read(zf)
            with open(target_path, 'wb') as f:
                f.write(data)
            restored += 1

print(f"Restored {restored} HTML files from 13.09.2026 backup!")
