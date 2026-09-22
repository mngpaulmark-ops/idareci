import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Inject upload_helper
if 'def upload_to_catbox' not in content:
    with open('upload_helper.py', 'r') as uf:
        helper = uf.read()
    content = content.replace('import os\n', 'import os\n' + helper + '\n')

# Add the proxy route
proxy_route = '''
@app.route('/files.catbox.moe/<path:filename>')
def catbox_proxy(filename):
    return redirect(f"https://files.catbox.moe/{filename}")
'''
if 'def catbox_proxy' not in content:
    content += proxy_route

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
