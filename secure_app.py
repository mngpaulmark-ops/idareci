import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

headers_code = """
@app.after_request
def add_security_headers(response):
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    # Block external unauthorized framing and sniffing
    return response
"""

if 'add_security_headers' not in content:
    content = content.replace('app = Flask(__name__)', 'app = Flask(__name__)\n' + headers_code)
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Security headers added.")
else:
    print("Security headers already exist.")
