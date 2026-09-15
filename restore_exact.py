import zipfile
import re

# Extract exact original app.py
with zipfile.ZipFile('C:/Users/turga/OneDrive/Desktop/bürokratlar birliği site yedeği/burokratlarbirligi_yedek_14.09.2026.zip') as z:
    original = z.read('app.py').decode('utf-8')

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(original)

print("Original app.py restored.")
