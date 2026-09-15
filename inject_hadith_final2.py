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
        if f.endswith('.html') or f.endswith('.htm'):
            path = os.path.join(root, f)
            try:
                with open(path, 'r', encoding='utf-8') as file:
                    content = file.read()
            except UnicodeDecodeError:
                continue
            
            if 'daily-hadith' not in content:
                # We want to put it right after the menu (Derneğimiz, vs) or at the end of the sidebar
                # The sidebar ends before <!-- sağ taraf son -->
                if '<!-- sağ taraf son -->' in content:
                    new_content = content.replace('<!-- sağ taraf son -->', hadith_html + '\n<!-- sağ taraf son -->', 1)
                    with open(path, 'w', encoding='utf-8') as file:
                        file.write(new_content)
                    count += 1
                elif '<!-- menu -->\n\t\t\t\t\n\t\t\t\t</div>' in content: # fallback
                    new_content = content.replace('<!-- menu -->\n\t\t\t\t\n\t\t\t\t</div>', '<!-- menu -->\n\t\t\t\t\n\t\t\t\t</div>\n' + hadith_html, 1)
                    with open(path, 'w', encoding='utf-8') as file:
                        file.write(new_content)
                    count += 1
                elif '<!-- sağ taraf  -->' in content:
                    # just append after the first panel
                    import re
                    new_content = re.sub(r'(<!-- sağ taraf  -->.*?</div>)', r'\1\n' + hadith_html, content, count=1, flags=re.DOTALL)
                    if new_content != content:
                        with open(path, 'w', encoding='utf-8') as file:
                            file.write(new_content)
                        count += 1
                        
print(f"Injected Hadith widget into {count} HTML files!")
