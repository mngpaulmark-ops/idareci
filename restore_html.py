import os
import zipfile

zip_path = r'C:\Users\turga\OneDrive\Desktop\bürokratlar birliği site yedeği\12_09_2026_yedek.zip'
base_dir = r'C:\Users\turga\OneDrive\Desktop\bürokratlar birliği site yedeği\burokratlarbirligi.org'

# Count 0-byte files
zero_byte_files = []
for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith('.html'):
            path = os.path.join(root, f)
            if os.path.getsize(path) == 0:
                rel_path = os.path.relpath(path, base_dir)
                zero_byte_files.append(rel_path.replace('\\', '/'))

print(f"Found {len(zero_byte_files)} zero-byte html files to restore.")

restored_count = 0
with zipfile.ZipFile(zip_path, 'r') as z:
    for zf in z.namelist():
        # The zip might have 'burokratlarbirligi.org/anasayfa.html'
        # Or just 'anasayfa.html'
        for rel in zero_byte_files:
            if zf.endswith(rel):
                try:
                    data = z.read(zf)
                    with open(os.path.join(base_dir, rel), 'wb') as out_f:
                        out_f.write(data)
                    restored_count += 1
                except Exception as e:
                    print(f"Failed to restore {rel}: {e}")
                break

print(f"Restored {restored_count} files from backup!")
