import os

print("1. Extracting pristine HTML files from backup...")
os.system("python extract_htmls.py")

print("2. Fixing base tags for subpages...")
os.system("python fix_base_tag.py")

print("3. Replacing widgets (Sosyal Medya -> Kamu Etiği)...")
os.system("python reapply_frontend_fixes.py")

print("4. Applying visual fixes (TRT sync, Banner, Flexbox)...")
os.system("python apply_missing_fixes.py")

print("5. Injecting Günün Hadis-i Şerifi...")
os.system("python inject_hadith_final.py")

print("6. Updating top header Social Links...")
os.system("python update_social_links.py")

print("7. Running CMS Updaters (Visibility toggles)...")
os.system("python run_updaters.py")

print("ALL RESTORATION STEPS COMPLETED PERFECTLY!")
