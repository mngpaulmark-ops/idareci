import bs4
import re

with open('anasayfa.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# Remove the bad CSS rule
text = re.sub(r'#trt-widget\s*{.*?}', '', text, flags=re.DOTALL)

with open('anasayfa.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Cleaned TRT widget CSS.")
