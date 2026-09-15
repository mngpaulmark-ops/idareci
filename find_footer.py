import glob
import re

for f in glob.glob('**/*.html', recursive=True):
    try:
        content = open(f, encoding='utf-8', errors='ignore').read()
        if '2015' in content and 'target="_blank"' in content:
            # check if they are close
            m = re.search(r'2015.*?target="_blank"', content, re.DOTALL)
            if m and len(m.group(0)) < 300:
                print(f)
                print(m.group(0))
                break
    except:
        pass
