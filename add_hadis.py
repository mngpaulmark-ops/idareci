import re

with open('templates/page.html', 'r', encoding='utf-8', errors='ignore') as f:
    page = f.read()

# Extract hadis block from page.html
match = re.search(r'(<div class="panel panel-primary hadis-i-serif".*?</div>\s*</div>)', page, re.DOTALL)
if not match:
    print("Could not find hadis block in page.html")
    exit()

hadis_block = match.group(1)

for html_file in ['anasayfa.html', 'resimler.html', 'videolar.html']:
    with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    if 'hadis-i-serif' not in content:
        # Insert before side-banner
        if '<div class="side-banner"' in content:
            content = content.replace('<div class="side-banner"', hadis_block + '\n <div class="side-banner"')
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Added hadis block to {html_file}")
        else:
            print(f"Could not find side-banner in {html_file}")
    else:
        print(f"hadis block already in {html_file}")

