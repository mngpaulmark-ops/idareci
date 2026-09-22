import requests

def upload_to_catbox(file_obj):
    try:
        resp = requests.post(
            'https://catbox.moe/user/api.php',
            data={'reqtype': 'fileupload'},
            files={'fileToUpload': (file_obj.filename, file_obj.read(), file_obj.content_type)}
        )
        if resp.status_code == 200:
            url = resp.text.strip()
            # url is https://files.catbox.moe/xyz
            # return 'files.catbox.moe/xyz'
            return url.replace('https://', '').replace('http://', '')
    except Exception as e:
        print("Catbox upload error:", e)
    return None
