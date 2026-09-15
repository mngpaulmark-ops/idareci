import re

with open('templates/page.html', 'r', encoding='utf-8', errors='ignore') as f:
    page = f.read()

# PROPER extraction of hadis block using bs4 to ensure it's fully closed
import bs4
soup_page = bs4.BeautifulSoup(page, 'html.parser')
hadis_div = soup_page.find('div', class_='hadis-i-serif')
hadis_block_correct = str(hadis_div)

for html_file in ['anasayfa.html', 'resimler.html', 'videolar.html']:
    with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    if 'hadis-i-serif' in content:
        # We need to remove the BROKEN hadis block which might be missing a closing tag.
        # The broken block was injected before <div class="side-banner"
        # It looks exactly like match.group(1) from before.
        # Let's just find where it starts:
        start_idx = content.find('<div class="panel panel-primary hadis-i-serif"')
        if start_idx != -1:
            end_idx = content.find('<div class="side-banner"', start_idx)
            if end_idx != -1:
                # Replace everything between start_idx and end_idx with the correct hadis block
                content = content[:start_idx] + hadis_block_correct + '\n ' + content[end_idx:]
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Fixed hadis block in {html_file}")
