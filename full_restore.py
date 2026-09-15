import os
import subprocess
import glob

# 1. Recover files
subprocess.run(['python', 'recover_files2.py'])

# 2. Fix mojibake
subprocess.run(['python', 'fix_mojibake.py'])

# 3. Update HTML from DB
subprocess.run(['python', 'update_page_html.py'])
subprocess.run(['python', 'update_temsilcilik_map.py'])
subprocess.run(['python', 'update_galeri_html.py'])
subprocess.run(['python', 'update_yonkur_templates.py'])

# 4. Apply manual injections
subprocess.run(['python', 'replace_social_with_academic.py'])
subprocess.run(['python', 'split_academic_panels.py'])
subprocess.run(['python', 'fix_widget_style_attr.py'])
subprocess.run(['python', 'inject_hadith_final.py'])

# 5. Fix CSS cache SAFELY
for file in glob.glob('*.html') + glob.glob('haber/*.html') + glob.glob('templates/*.html'):
    if os.path.isfile(file):
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
            if 'css/style.css"' in content or "css/style.css'" in content or 'css/style.css?' in content:
                import re
                new_content = re.sub(r'css/style\.css(\?v=\d+)?', 'css/style.css?v=4', content)
                with open(file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
        except:
            pass

# 6. Apply visibility toggles from DB
subprocess.run(['python', '-c', 'from app import update_widgets_html, update_sidebar_html, update_video_html, apply_menus_to_all_html; update_widgets_html(); update_sidebar_html(); update_video_html(); apply_menus_to_all_html()'])

print("Full restore complete!")
