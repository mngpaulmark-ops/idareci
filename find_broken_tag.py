import glob
import os

count = 0
for f in glob.glob('**/*.html', recursive=True):
    try:
        content = open(f, encoding='utf-8', errors='ignore').read()
        if '/" title="" target="_blank">' in content:
            print(f)
            count += 1
            if count >= 10:
                break
    except:
        pass
