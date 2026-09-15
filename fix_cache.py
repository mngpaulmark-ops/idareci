import re

with open('app.py', 'r', encoding='utf-8', errors='surrogateescape') as f:
    code = f.read()

no_cache_code = """@app.route('/<path:filename>')
def serve_static(filename):
    from flask import make_response
    if os.path.exists(filename):
        resp = make_response(send_from_directory('.', filename))
    elif os.path.exists(filename + '.html'):
        resp = make_response(send_from_directory('.', filename + '.html'))
    elif os.path.exists(filename + '.htm'):
        resp = make_response(send_from_directory('.', filename + '.htm'))
    else:
        return "Not Found", 404
        
    resp.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    resp.headers['Pragma'] = 'no-cache'
    resp.headers['Expires'] = '0'
    return resp
"""

if "no-store, must-revalidate" not in code:
    code = re.sub(r'@app\.route\(\'/<path:filename>\'\)\ndef serve_static\(filename\):.*?return "Not Found", 404\s*', no_cache_code, code, flags=re.DOTALL)
    
with open('app.py', 'w', encoding='utf-8', errors='surrogateescape') as f:
    f.write(code)
print("Updated serve_static to prevent caching.")
