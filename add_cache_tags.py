with open('templates/admin/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace('<head>', '<head>\n    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />\n    <meta http-equiv="Pragma" content="no-cache" />\n    <meta http-equiv="Expires" content="0" />')

with open('templates/admin/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Added cache busting tags.")
