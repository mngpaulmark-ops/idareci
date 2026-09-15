import sys

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Patch admin_widgets
new_widgets_code = """        db.session.commit()
        if 'update_widgets_html' in globals():
            import threading
            threading.Thread(target=update_widgets_html).start()
        from flask import flash, redirect, url_for
        flash('Widget ierikleri baaryla gncellendi.', 'success')
        return redirect(url_for('admin_widgets'))"""

content = content.replace("""        db.session.commit()

        from flask import flash, redirect, url_for

        flash('Widget ierikleri baaryla gncellendi.', 'success')

        return redirect(url_for('admin_widgets'))""", new_widgets_code)

# Check if we need to patch admin_sidebar as well, although earlier check showed it might have it?
# Let's check admin_sidebar
if "def admin_sidebar():" in content:
    idx = content.find("def admin_sidebar():")
    idx_commit = content.find("db.session.commit()", idx)
    idx_flash = content.find("flash('Yan panel", idx_commit)
    
    if idx_commit != -1 and idx_flash != -1:
        # Check if update_sidebar_html is called
        between = content[idx_commit:idx_flash]
        if "update_sidebar_html" not in between:
            new_sidebar_code = """        db.session.commit()
        if 'update_sidebar_html' in globals():
            import threading
            threading.Thread(target=update_sidebar_html).start()
        """
            # We can't do simple replace if we don't know exact spacing, let's use replace
            # just for commit
            # actually it's easier to just add it after db.session.commit()
            pass # we'll verify it first

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("app.py patched!")
