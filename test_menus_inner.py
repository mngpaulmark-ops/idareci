import app
app.app.config['TESTING'] = True

try:
    with app.app.app_context():
        app._apply_menus_inner()
    print("Success")
except Exception as e:
    import traceback
    traceback.print_exc()
