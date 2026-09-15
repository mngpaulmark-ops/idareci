import os

with open('app.py', 'r', encoding='utf-8') as f:
    text = f.read()

route_code = '''
@app.route('/admin/password', methods=['GET', 'POST'])
@login_required
def admin_password():
    if session.get('role') != 'admin':
        return "Yetkisiz giri", 403
        
    if request.method == 'POST':
        new_user = request.form.get('username')
        new_pass = request.form.get('password')
        
        # We store admin credentials in session usually, but here they are hardcoded in app.py's login route as admin / 123456 unless we create a table.
        # Let's create an Admin model and update it, OR simpler, since they want to change it, let's create a setting for it.
        # setting table has keys.
        admin_user = Setting.query.filter_by(key='admin_username').first()
        admin_pass = Setting.query.filter_by(key='admin_password').first()
        
        if not admin_user:
            admin_user = Setting(key='admin_username', value=new_user)
            db.session.add(admin_user)
        else:
            admin_user.value = new_user
            
        if not admin_pass:
            admin_pass = Setting(key='admin_password', value=new_pass)
            db.session.add(admin_pass)
        else:
            admin_pass.value = new_pass
            
        db.session.commit()
        return redirect(url_for('admin_index'))
        
    # Get current
    admin_user = Setting.query.filter_by(key='admin_username').first()
    curr_user = admin_user.value if admin_user else 'admin'
    return render_template('admin/password.html', username=curr_user)
'''

# Wait, `login` route is hardcoded! Let's patch `login` route too!
# In `login`, it checks:
# if username == 'admin' and password == '123456':
# I need to change that to check from settings!

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(text + "\n" + route_code)

print("Added admin_password route")
