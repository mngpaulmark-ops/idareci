import glob
import re
import os

left_widget_html = '''<div class="panel panel-sto panel-primary" id="panel-kamu-etigi">
    <div class="panel-heading" style="background-color: #2980b9;">
        <i class="glyphicon glyphicon-education" style="font-size: 16px; margin-right: 8px;"></i> Kamu Etiği ve Yönetim İlkeleri
    </div>
    <div class="panel-body" style="padding: 15px;">
        <div style="background-color: #f9f9f9; padding: 12px; margin-bottom: 5px; border-radius: 4px;">
            <p style="font-size: 14px; color: #555; margin-bottom: 12px;">Kamuda etik değerler ve şeffaf yönetim anlayışı üzerine düzenlenen güncel seminer programlarımız.</p>
            <a href="#" class="btn btn-primary btn-sm" style="background-color: #2980b9; border:none; width: 100%;">Detayları İncele <i class="glyphicon glyphicon-chevron-right"></i></a>
        </div>
    </div>
</div>'''

right_widget_html = '''<div class="panel panel-sto panel-danger" id="panel-yonetim-liderlik">
    <div class="panel-heading" style="background-color: #e74c3c; color: white;">
        <i class="glyphicon glyphicon-blackboard" style="font-size: 16px; margin-right: 8px;"></i> Yönetim ve Liderlik Seminerleri
    </div>
    <div class="panel-body" style="padding: 15px;">
        <div style="background-color: #f9f9f9; padding: 12px; border-radius: 4px;">
            <p style="font-size: 14px; color: #555; margin-bottom: 12px;">Geleceğin yöneticilerini yetiştiren vizyoner liderlik eğitimleri ve akademik panel serileri.</p>
            <a href="#" class="btn btn-danger btn-sm" style="background-color: #e74c3c; border:none; width: 100%;">Seminerlere Git <i class="glyphicon glyphicon-chevron-right"></i></a>
        </div>
    </div>
</div>'''

count = 0

# 1. Clean Tuncer Unal metadata and name
print("Cleaning Tuncer Unal references...")
for root, dirs, files in os.walk('.'):
    if '.git' in root or '__pycache__' in root or 'venv' in root or 'instance' in root: continue
    for f in files:
        if f.endswith('.html'):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8', errors='surrogateescape') as file:
                content = file.read()
            
            if not content: continue
            
            new_content = re.sub(r'<meta[^>]*tuncer[^>]*>\n?', '', content, flags=re.IGNORECASE)
            new_content = re.sub(r'tuncer\s+nal', 'Yazar', new_content, flags=re.IGNORECASE)
            new_content = re.sub(r'tuncer\s+unal', 'Yazar', new_content, flags=re.IGNORECASE)
            new_content = re.sub(r'Tuncer\s+onal', 'Yazar', new_content, flags=re.IGNORECASE)
            new_content = re.sub(r'Tuncer\s+Ünal', 'Yazar', new_content, flags=re.IGNORECASE)
            
            if content != new_content:
                with open(path, 'w', encoding='utf-8', errors='surrogateescape') as file:
                    file.write(new_content)
                count += 1

print(f"Cleaned {count} HTML files!")

# 2. Replace Sosyal Medya and Hava Durumu in anasayfa.html safely using regex
print("Replacing Sosyal Medya and Hava Durumu widgets in anasayfa.html...")
with open('anasayfa.html', 'r', encoding='utf-8', errors='surrogateescape') as f:
    page = f.read()

# Sosyal Medya block
sm_pattern = r'(<div class="panel panel-sto panel-light-red piyasaverileri">.*?Sosyal Medya.*?<div class="panel-body">.*?)(</div>\s*</div>\s*</div>)'
sm_match = re.search(sm_pattern, page, flags=re.DOTALL)
if sm_match:
    page = re.sub(sm_pattern, left_widget_html, page, flags=re.DOTALL)
    print("Replaced Sosyal Medya!")
else:
    # Try a looser match
    sm_pattern2 = r'<div class="panel panel-sto panel-light-red piyasaverileri">.*?Sosyal Medya.*?</div>\s*</div>'
    if re.search(sm_pattern2, page, flags=re.DOTALL):
        page = re.sub(sm_pattern2, left_widget_html, page, flags=re.DOTALL)
        print("Replaced Sosyal Medya (looser)!")
    
# Hava Durumu block
hd_pattern = r'(<div class="panel panel-sto panel-cyan">.*?Hava Durumu.*?<div class="panel-body">.*?)(</div>\s*</div>)'
hd_match = re.search(hd_pattern, page, flags=re.DOTALL)
if hd_match:
    page = re.sub(hd_pattern, right_widget_html, page, flags=re.DOTALL)
    print("Replaced Hava Durumu!")
else:
    hd_pattern2 = r'<div class="panel panel-sto panel-cyan">.*?Hava Durumu.*?</div>\s*</div>\s*</div>'
    if re.search(hd_pattern2, page, flags=re.DOTALL):
        page = re.sub(hd_pattern2, right_widget_html, page, flags=re.DOTALL)
        print("Replaced Hava Durumu (looser)!")

with open('anasayfa.html', 'w', encoding='utf-8', errors='surrogateescape') as f:
    f.write(page)

print("Widgets applied!")
