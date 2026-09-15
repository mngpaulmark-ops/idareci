import glob
import re

pattern = r'<nav class="collapse navbar-collapse bs-navbar-collapse" id="bs-example-navbar-collapse-1">\s*<ul class="nav navbar-nav">.*?</ul>\s*</nav>'

files = glob.glob('*.html') + glob.glob('haber/*.html')
failed = []
for f in files:
    content = open(f, encoding='utf-8', errors='ignore').read()
    if '<ul class="nav navbar-nav">' in content: # It HAS a menu
        if not re.search(pattern, content, flags=re.DOTALL):
            failed.append(f)

print("Failed count:", len(failed))
if failed:
    print("First 10 failed:", failed[:10])
    
    # Show what it actually looks like in one of the failed files
    content = open(failed[0], encoding='utf-8', errors='ignore').read()
    match = re.search(r'<nav[^>]*>.*?<ul class="nav navbar-nav">.*?</ul>.*?</nav>', content, flags=re.DOTALL)
    if match:
        print("Actual HTML around nav:")
        print(match.group(0)[:200])
