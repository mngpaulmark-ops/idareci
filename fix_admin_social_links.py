import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the parsing of Facebook and Twitter links in admin_settings
pattern = r"fb_tag = soup\.find\('a', class_='facebook'\)\n\s+if fb_tag: fb_link = fb_tag\.get\('href'\)\n\s+tw_tag = soup\.find\('a', class_='twitter'\)\n\s+if tw_tag: tw_link = tw_tag\.get\('href'\)"
replacement = r"""fb_tag = soup.find('a', lambda tag: tag and tag.get('title') and 'Facebook' in tag.get('title'))
            if fb_tag: fb_link = fb_tag.get('href')
            tw_tag = soup.find('a', lambda tag: tag and tag.get('title') and 'Twitter' in tag.get('title'))
            if tw_tag: tw_link = tw_tag.get('href')"""

content = re.sub(pattern, replacement, content)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated app.py to correctly parse social links.")
