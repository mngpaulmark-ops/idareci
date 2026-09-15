import re

with open('anasayfa.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

hadith_html = """<div class="widget mb-4" style="margin-top:20px;"><h3 class="widget-title font-weight-bold" style="color:#800000; border-bottom:2px solid #800000; padding-bottom:5px; margin-bottom:15px;">Günün Hadisi</h3><div id="daily-hadith" style="padding:15px; background-color:#f9f9f9; border-radius:5px; font-style:italic; border-left:4px solid #800000; min-height:100px;"></div></div><script>const hadiths=["Ameller niyetlere göredir.", "Sizin en hayırlınız Kur'an'ı öğrenen ve öğretendir.", "İman yetmiş küsur şubedir.", "Müslüman, elinden ve dilinden diğer Müslümanların güvende olduğu kimsedir.", "Kim Allah'a ve ahiret gününe inanıyorsa komşusuna iyilik etsin.", "Kolaylaştırın, zorlaştırmayın; müjdeleyin, nefret ettirmeyin.", "Din nasihattir.", "Söz taşıyanlar cennete giremez.", "Merhamet etmeyene merhamet edilmez.", "İşçiye ücretini teri kurumadan veriniz."]; const day = Math.floor((new Date()-new Date(new Date().getFullYear(),0,0))/1000/60/60/24); document.getElementById("daily-hadith").innerText = hadiths[day % hadiths.length];</script>"""

# Find `</div> <!-- .panel .panel-primary -->` and insert hadith_html right after it
if "Günün Hadisi" not in content:
    content = content.replace('</div> <!-- .panel .panel-primary -->', '</div> <!-- .panel .panel-primary -->\n' + hadith_html)
    
    with open('anasayfa.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Hadith widget added!")
else:
    print("Hadith widget already exists!")
