with open('app.py', 'r', encoding='utf-8') as f:
    text = f.read()

old_return = "return render_template('admin/settings.html', facebook=fb_link, twitter=tw_link)"
new_return = """    settings = {
        'facebook': {'label': 'Facebook Adresi', 'value': fb_link},
        'twitter': {'label': 'Twitter Adresi', 'value': tw_link}
    }
    return render_template('admin/settings.html', settings=settings)"""

if old_return in text:
    text = text.replace(old_return, new_return)
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Fixed settings in app.py')
else:
    print('String not found in app.py')
