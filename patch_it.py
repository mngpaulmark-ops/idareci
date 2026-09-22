import re
with open('app.py', 'r', encoding='utf-8') as f:
    c = f.read()

new_func = '''def upload_to_catbox(file_obj):
    from flask import flash
    try:
        file_data = file_obj.read()
        resp = requests.post(
            'https://catbox.moe/user/api.php',
            data={'reqtype': 'fileupload'},
            files={'fileToUpload': (file_obj.filename, file_data, file_obj.content_type)},
            timeout=15
        )
        if resp.status_code == 200:
            url = resp.text.strip()
            return url.replace('https://', '').replace('http://', '')
        else:
            flash("Resim yukleme hatasi (Bulut reddetti): " + str(resp.status_code))
            return None
    except Exception as e:
        flash("Resim yukleme baglanti hatasi")
        return None'''

c = re.sub(r'def upload_to_catbox\(file_obj\):.*?return None', new_func, c, flags=re.DOTALL)
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(c)
