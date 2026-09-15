import re

with open('app.py', 'r', encoding='utf-8', errors='surrogateescape') as f:
    code = f.read()

# 1. EditorUser model
if 'can_galeri = db.Column(db.Boolean, default=False)' not in code:
    code = code.replace("can_kose = db.Column(db.Boolean, default=False)", "can_kose = db.Column(db.Boolean, default=False)\n    can_galeri = db.Column(db.Boolean, default=False)\n    can_video = db.Column(db.Boolean, default=False)")

# 2. check_editor_permission
if 'if module == \'galeri\' and ed.can_galeri: return True' not in code:
    code = code.replace("if module == 'kose' and ed.can_kose: return True", "if module == 'kose' and ed.can_kose: return True\n        if module == 'galeri' and ed.can_galeri: return True\n        if module == 'video' and ed.can_video: return True")

# 3. admin_editors add/edit logic
if "cg = request.form.get('can_galeri') == 'on'" not in code:
    code = code.replace("ck = request.form.get('can_kose') == 'on'", "ck = request.form.get('can_kose') == 'on'\n        cg = request.form.get('can_galeri') == 'on'\n        cv = request.form.get('can_video') == 'on'")
    
    code = code.replace("can_kose=ck))", "can_kose=ck, can_galeri=cg, can_video=cv))")
    
    code = code.replace("ed.can_kose = ck", "ed.can_kose = ck\n            ed.can_galeri = cg\n            ed.can_video = cv")

# 4. Route protections
# Wait, I previously injected `if session.get('role') != 'admin': return redirect(url_for('admin_index'))` into some routes, including admin_galeri? No, I injected it into `admin_widgets`, etc.
# But for admin_galeri, let's inject check_editor_permission.
def inject_permission(route_func, module):
    global code
    search = f"def {route_func}():\n"
    if search in code:
        if f"check_editor_permission('{module}')" not in code.split(search)[1].split('\n')[0]:
            replacement = f"def {route_func}():\n    if not check_editor_permission('{module}'): return redirect(url_for('admin_index'))\n"
            code = code.replace(search, replacement)
    
    search_id = f"def {route_func}(id):\n"
    if search_id in code:
        if f"check_editor_permission('{module}')" not in code.split(search_id)[1].split('\n')[0]:
            replacement = f"def {route_func}(id):\n    if not check_editor_permission('{module}'): return redirect(url_for('admin_index'))\n"
            code = code.replace(search_id, replacement)

inject_permission('admin_galeri', 'galeri')
inject_permission('admin_galeri_ekle', 'galeri')
inject_permission('admin_galeri_detay', 'galeri')
inject_permission('admin_galeri_resimsil', 'galeri')
inject_permission('admin_videos', 'video')
inject_permission('admin_video_delete', 'video')

with open('app.py', 'w', encoding='utf-8', errors='surrogateescape') as f:
    f.write(code)
print("Updated app.py with galeri and video permissions.")
