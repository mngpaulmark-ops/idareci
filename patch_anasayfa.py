import re

with open('anasayfa.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Replace Poll with Hadith
poll_pattern = r'<div class="anket">.*?</div><!-- \.anket -->'
hadith_html = """<div class="anket widget mb-4"><h3 class="widget-title font-weight-bold" style="color:#800000; border-bottom:2px solid #800000; padding-bottom:5px; margin-bottom:15px;">Günün Hadisi</h3><div id="daily-hadith" style="padding:15px; background-color:#f9f9f9; border-radius:5px; font-style:italic; border-left:4px solid #800000; min-height:100px;"></div></div><script>const hadiths=["Ameller niyetlere göredir.", "Sizin en hayırlınız Kur'an'ı öğrenen ve öğretendir.", "İman yetmiş küsur şubedir.", "Müslüman, elinden ve dilinden diğer Müslümanların güvende olduğu kimsedir.", "Kim Allah'a ve ahiret gününe inanıyorsa komşusuna iyilik etsin.", "Kolaylaştırın, zorlaştırmayın; müjdeleyin, nefret ettirmeyin.", "Din nasihattir.", "Söz taşıyanlar cennete giremez.", "Merhamet etmeyene merhamet edilmez.", "İşçiye ücretini teri kurumadan veriniz."]; const day = Math.floor((new Date()-new Date(new Date().getFullYear(),0,0))/1000/60/60/24); document.getElementById("daily-hadith").innerText = hadiths[day % hadiths.length];</script>"""

content = re.sub(poll_pattern, hadith_html, content, flags=re.DOTALL)

# Replace social links
content = re.sub(r'href="[^"]*facebook.com[^"]*"', 'href="https://www.facebook.com/Burokratlarbirligi-327956840549801/"', content)
content = re.sub(r'href="[^"]*twitter.com[^"]*"', 'href="#"', content)

with open('anasayfa.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("anasayfa.html restored!")
