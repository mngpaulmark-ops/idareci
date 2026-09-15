import re

script_code = """
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

for html_file in ['anasayfa.html', 'resimler.html', 'videolar.html']:
    with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    if 'hadiths[day % hadiths.length]' not in content:
        # Find the end of the hadis block
        # We know hadis ends right before <div class="side-banner" in these files.
        idx = content.find('<div class="side-banner"')
        if idx != -1:
            content = content[:idx] + script_code + '\n ' + content[idx:]
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Added script to {html_file}")
    else:
        print(f"Script already in {html_file}")
