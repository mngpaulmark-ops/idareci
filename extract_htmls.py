import zipfile
import os

print("Extracting all html files from backup...")
z = zipfile.ZipFile(r'C:\Users\turga\OneDrive\Desktop\burokratlarbirligi_yedek_13.09.2026.zip')

for info in z.infolist():
    if info.filename.endswith('.html') and not info.filename.startswith('__MACOSX'):
        z.extract(info, '.')

print("Done extracting!")
