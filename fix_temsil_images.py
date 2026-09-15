import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the two instances of f"uploads/{unique_filename}"
content = content.replace('f"uploads/{unique_filename}"', 'f"data/uploads/{unique_filename}"')

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated app.py image paths for Temsilcilik.")

# Now fix the database records
import app
with app.app.app_context():
    reps = app.Temsilcilik.query.all()
    changed = False
    for r in reps:
        if r.image_path and r.image_path.startswith('uploads/'):
            r.image_path = 'data/' + r.image_path
            changed = True
    if changed:
        app.db.session.commit()
        print("Updated database records.")
    
    # Regenerate temsilcilik.html
    import temsil_helper
    print("Regenerated temsilcilik.html via temsil_helper.")
