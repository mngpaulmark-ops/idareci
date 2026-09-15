import re
with open('templates/page.html', 'r', encoding='utf-8', errors='ignore') as f:
    page = f.read()

match = re.search(r'(<div class="panel panel-primary hadis-i-serif".*?</div>\s*</div>)', page, re.DOTALL)
print(repr(match.group(1)))
