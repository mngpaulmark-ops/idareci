import zipfile
import re

# 1. Restore the ENTIRE old app.py
with zipfile.ZipFile('C:/Users/turga/OneDrive/Desktop/bürokratlar birliği site yedeği/burokratlarbirligi_yedek_14.09.2026.zip') as z:
    app_content = z.read('app.py').decode('utf-8')

# 2. Fix the Haber sorting query
app_content = app_content.replace("Haber.query.order_by(Haber.id.desc()).all()", "Haber.query.order_by(Haber.date.desc(), Haber.id.desc()).all()")
app_content = app_content.replace("Haber.query.order_by(Haber.id.desc()).limit(10).all()", "Haber.query.order_by(Haber.date.desc(), Haber.id.desc()).limit(10).all()")

# 3. Fix the Haber slug and date parsing in admin_haber_add
old_add = """        slug = request.form.get('slug', '')
        if not slug:
            # Generate basic slug
            slug = title.lower().replace(' ', '-').replace('ı', 'i').replace('ö', 'o').replace('ü', 'u').replace('ş', 's').replace('ğ', 'g').replace('ç', 'c')
            slug = "".join(c for c in slug if c.isalnum() or c == '-')
        
        h = Haber(title=title, content=content, slug=slug)
        file = request.files.get('file')"""

new_add = """        slug = request.form.get('slug', '')
        if not slug:
            # Generate basic slug
            slug = title.lower().replace(' ', '-').replace('ı', 'i').replace('ö', 'o').replace('ü', 'u').replace('ş', 's').replace('ğ', 'g').replace('ç', 'c')
            slug = "".join(c for c in slug if c.isalnum() or c == '-')
        
        date_str = request.form.get('date')
        h = Haber(title=title, content=content, slug=slug)
        if date_str:
            import datetime
            try:
                h.date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
            except:
                pass
        
        file = request.files.get('image')"""

app_content = app_content.replace(old_add, new_add)

# 4. Fix the Haber slug and date parsing in admin_haber_edit
old_edit = """        h.title = request.form.get('title')
        h.content = request.form.get('content')
        file = request.files.get('file')"""

new_edit = """        h.title = request.form.get('title')
        h.content = request.form.get('content')
        slug = request.form.get('slug')
        if slug:
            h.slug = slug
        date_str = request.form.get('date')
        if date_str:
            import datetime
            try:
                h.date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
            except:
                pass
        file = request.files.get('image')"""

app_content = app_content.replace(old_edit, new_edit)

# 5. Fix tracebacks in try/except blocks (replace 'except: pass' with traceback)
app_content = app_content.replace("""        except:
            pass""", """        except Exception as e:
            import traceback
            traceback.print_exc()""")

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(app_content)
print("Fully restored app.py with selective Haber fixes")
