import re
import os

hadith_html = """
<div class="panel panel-primary hadis-i-serif" style="margin-top: 20px; border-color: #800000; box-shadow: 0 4px 8px rgba(0,0,0,0.05);">
    <div class="panel-heading" style="background-color: #800000; border-color: #800000; color: white; font-weight: bold; font-size: 15px; padding: 12px 15px;">
        <i class="fa fa-book" aria-hidden="true" style="margin-right:8px;"></i> Günün Hadis-i Şerifi
    </div>
    <div class="panel-body" style="background-color: #fdfaf6; padding: 25px 20px;">
        <div style="text-align: center; color: #800000; font-size: 20px; margin-bottom: 12px; opacity: 0.6;">
            <i class="fa fa-quote-left" aria-hidden="true"></i>
        </div>
        <div id="daily-hadith" style="font-size: 16px; font-style: italic; font-weight: 600; color: #444; line-height: 1.7; text-align: center; font-family: 'Georgia', 'Times New Roman', serif;">
        </div>
        <div style="text-align: center; color: #800000; font-size: 20px; margin-top: 12px; opacity: 0.6;">
            <i class="fa fa-quote-right" aria-hidden="true"></i>
        </div>
    </div>
</div>
<script>
const hadiths = [
    "Ameller niyetlere göredir.", 
    "Sizin en hayırlınız Kur'an'ı öğrenen ve öğretendir.", 
    "İman yetmiş küsur şubedir.", 
    "Müslüman, elinden ve dilinden diğer Müslümanların güvende olduğu kimsedir.", 
    "Kim Allah'a ve ahiret gününe inanıyorsa komşusuna iyilik etsin.", 
    "Kolaylaştırın, zorlaştırmayın; müjdeleyin, nefret ettirmeyin.", 
    "Din nasihattir.", 
    "Söz taşıyanlar cennete giremez.", 
    "Merhamet etmeyene merhamet edilmez.", 
    "İşçiye ücretini teri kurumadan veriniz."
]; 
const day = Math.floor((new Date() - new Date(new Date().getFullYear(),0,0)) / 1000 / 60 / 60 / 24); 
document.getElementById("daily-hadith").innerText = hadiths[day % hadiths.length];
</script>"""

count = 0

for root, dirs, files in os.walk('.'):
    if '.git' in root or '__pycache__' in root or 'venv' in root or 'instance' in root: continue
    for f in files:
        if f.endswith('.html'):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8', errors='surrogateescape') as file:
                content = file.read()
            
            if 'daily-hadith' not in content:
                # Insert right after the Derneğimiz menu
                if '</div> <!-- .panel .panel-primary -->' in content:
                    new_content = content.replace('</div> <!-- .panel .panel-primary -->', '</div> <!-- .panel .panel-primary -->\n' + hadith_html, 1)
                    with open(path, 'w', encoding='utf-8', errors='surrogateescape') as file:
                        file.write(new_content)
                    count += 1

print(f"Injected Hadith widget into {count} HTML files!")
