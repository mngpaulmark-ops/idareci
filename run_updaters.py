import sys
sys.path.insert(0, '.')
from app import app, db, update_widgets_html, update_sidebar_html, update_video_html, apply_menus_to_all_html

with app.app_context():
    print("Running updaters on fresh anasayfa.html...")
    update_widgets_html()
    update_sidebar_html()
    update_video_html()
    print("Done!")
