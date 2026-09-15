from app import app, db
import app as myapp

with app.app_context():
    db.create_all()
    print("Database updated.")
    
    # Run all HTML updates so current settings are reflected!
    try:
        if hasattr(myapp, 'update_widgets_html'):
            myapp.update_widgets_html()
            print("Widgets updated.")
        if hasattr(myapp, 'update_sidebar_html'):
            myapp.update_sidebar_html()
            print("Sidebar updated.")
        if hasattr(myapp, 'update_video_html'):
            myapp.update_video_html()
            print("Video updated.")
        if hasattr(myapp, 'apply_menus_to_all_html'):
            myapp.apply_menus_to_all_html()
            print("Menus updated.")
    except Exception as e:
        print(f"Error during updates: {e}")
