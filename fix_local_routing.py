import re

with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

target = """@app.route('/<path:filename>')
def serve_static(filename):"""

injection = """@app.route('/idareci/')
@app.route('/idareci/<path:filename>')
def serve_idareci(filename=''):
    if not filename or filename == '/':
        return send_from_directory('.', 'anasayfa.html')
    if os.path.exists(filename):
        return send_from_directory('.', filename)
    elif os.path.exists(filename + '.html'):
        return send_from_directory('.', filename + '.html')
    elif os.path.exists(filename + '.htm'):
        return send_from_directory('.', filename + '.htm')
    else:
        from flask import abort
        abort(404)

@app.route('/<path:filename>')
def serve_static(filename):"""

code = code.replace(target, injection)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Added /idareci/ static file route alias!")
