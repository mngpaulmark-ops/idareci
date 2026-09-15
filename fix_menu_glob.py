with open('app.py', 'r', encoding='utf-8') as f:
    app_content = f.read()

# Let's fix the glob.glob list in apply_menus_to_all_html
old_glob = "for file in glob.glob('*.html') + glob.glob('haber/*.html') + glob.glob('templates/*.html'):"
new_glob = "for file in glob.glob('*.html') + glob.glob('haber/*.html') + glob.glob('templates/*.html') + glob.glob('koseyazisi/**/*.html', recursive=True):"

if old_glob in app_content:
    app_content = app_content.replace(old_glob, new_glob)
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(app_content)
    print("Replaced glob in apply_menus_to_all_html")
else:
    print("Could not find glob line.")
