import re

with open('app.py', 'r', encoding='utf-8') as f:
    c = f.read()

c = re.sub(
    r'file\.save\(file_path\)\s*return jsonify\(\{''location'': f''/data/uploads/\{filename\}''\}\)',
    r'''catbox_path = upload_to_catbox(file)
        if catbox_path:
            return jsonify({'location': f'/{catbox_path}'})
        file.save(file_path)
        return jsonify({'location': f'/data/uploads/{filename}'})''', c
)

c = re.sub(
    r'file\.save\(os\.path\.join\(upload_folder, filename\)\)\s*m\.image_path = f''data/yonkur_uploads/\{filename\}''',
    r'''catbox_path = upload_to_catbox(file)
            if catbox_path:
                m.image_path = catbox_path
            else:
                file.save(os.path.join(upload_folder, filename))
                m.image_path = f'data/yonkur_uploads/{filename}'''', c
)

c = re.sub(
    r'file\.save\(path\)\s*img_path = ''data/page/'' \+ filename',
    r'''catbox_path = upload_to_catbox(file)
        if catbox_path:
            img_path = catbox_path
        else:
            file.save(path)
            img_path = 'data/page/' + filename''', c
)

c = re.sub(
    r'file\.save\(path\)\s*db\.session\.add\(GaleriResim\(galeri_id=id, image_path=''data/page/''\+filename\)\)',
    r'''catbox_path = upload_to_catbox(file)
                if catbox_path:
                    db.session.add(GaleriResim(galeri_id=id, image_path=catbox_path))
                else:
                    file.save(path)
                    db.session.add(GaleriResim(galeri_id=id, image_path='data/page/'+filename))''', c
)

c = re.sub(
    r'file\.save\(os\.path\.join\(app\.config\[''UPLOAD_FOLDER''\], filename\)\)\s*image_path = ''data/uploads/'' \+ filename',
    r'''catbox_path = upload_to_catbox(file)
            if catbox_path:
                image_path = catbox_path
            else:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_path = 'data/uploads/' + filename''', c
)

c = re.sub(
    r'file\.save\(os\.path\.join\(app\.config\[''UPLOAD_FOLDER''\], filename\)\)\s*haber\.image_path = ''data/uploads/'' \+ filename',
    r'''catbox_path = upload_to_catbox(file)
            if catbox_path:
                haber.image_path = catbox_path
            else:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                haber.image_path = 'data/uploads/' + filename''', c
)

c = re.sub(
    r'image\.save\(os\.path\.join\(app\.config\[''UPLOAD_FOLDER''\], unique_filename\)\)\s*image_path = f"uploads/\{unique_filename\}"',
    r'''catbox_path = upload_to_catbox(image)
            if catbox_path:
                image_path = catbox_path
            else:
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
                image_path = f"uploads/{unique_filename}"''', c
)

c = re.sub(
    r'image\.save\(os\.path\.join\(app\.config\[''UPLOAD_FOLDER''\], unique_filename\)\)\s*rep\.image_path = f"data/uploads/\{unique_filename\}"',
    r'''catbox_path = upload_to_catbox(image)
                if catbox_path:
                    rep.image_path = catbox_path
                else:
                    image.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
                    rep.image_path = f"data/uploads/{unique_filename}"''', c
)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(c)
