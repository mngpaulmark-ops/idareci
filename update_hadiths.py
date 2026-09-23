import os
import re

new_script = """<script>
const hadiths = [
    "Ameller ancak niyetlere göredir; herkesin niyeti ne ise eline geçecek odur. (Buhârî, Bed'ü'l-vahy 1)",
    "Sizin en hayırlınız, ahlakı en güzel olanınızdır. (Buhârî, Edeb 38)",
    "Hiçbiriniz kendisi için istediğini, mümin kardeşi için de istemedikçe gerçek anlamda iman etmiş olamaz. (Buhârî, Îmân 7)",
    "Kim Allah'a ve ahiret gününe inanıyorsa komşusuna iyilik etsin. (Müslim, Îmân 74)",
    "Kolaylaştırın, zorlaştırmayın; müjdeleyin, nefret ettirmeyin. (Buhârî, İlim 11)",
    "Allah'a yemin ederim ki; siz iman etmedikçe cennete giremezsiniz. Birbirinizi sevmedikçe de gerçek anlamda iman etmiş olamazsınız. (Müslim, Îmân 93)",
    "Müslüman, elinden ve dilinden diğer Müslümanların güvende olduğu kimsedir. (Buhârî, Îmân 4)",
    "Her kim bir Müslümanın ayıbını örterse, Allah da kıyamet günü onun ayıbını örter. (Müslim, Zikir 38)",
    "Merhamet etmeyene merhamet edilmez. (Buhârî, Edeb 18)",
    "Dul ve fakirlere yardım eden kimse, Allah yolunda cihad eden, gündüzleri oruçla, geceleri ibadetle geçiren kimse gibidir. (Buhârî, Nafakât 1)",
    "İki nimet vardır ki, insanların çoğu bu nimetleri kullanmakta aldanmıştır: Sıhhat ve boş vakit. (Buhârî, Rikak 1)",
    "Mü'minin durumu gıpta ve hayranlığa değer. Çünkü her hali kendisi için bir hayır sebebidir. Böylesi bir özellik sadece mü'minde vardır... (Müslim, Zühd 64)",
    "Şüphesiz Allah, sizin suretlerinize ve mallarınıza bakmaz; ancak kalplerinize ve amellerinize bakar. (Müslim, Birr 34)",
    "Güçlü kimse, güreşte hasmını yenen değil, öfkelendiği zaman nefsine hâkim olandır. (Buhârî, Edeb 76)",
    "Söz taşıyanlar (nemmâm) cennete giremez. (Müslim, Îmân 168)",
    "Yarım hurma (sadaka) ile de olsa cehennem ateşinden korununuz. Onu da bulamazsanız, tatlı ve güzel sözle (korununuz). (Buhârî, Edeb 34)",
    "Kim bir hidayete (doğru yola) çağrıda bulunursa, ona uyanların sevaplarının birer misli ona da verilir. (Müslim, İlim 16)",
    "Sıla-i rahim yapan, akrabasından gördüğü iyiliğe karşılık veren kimse değildir; asıl sıla-i rahim yapan, kendisiyle ilişkiyi kestikleri halde akrabasını görüp gözetendir. (Buhârî, Edeb 15)",
    "Allahım! Seni zikretmek, sana şükretmek ve sana güzelce ibadet etmekte bana yardım et! (Ebû Dâvûd, Vitir 26)",
    "Her iyilik bir sadakadır. (Buhârî, Edeb 33)",
    "İşçiye ücretini teri kurumadan veriniz. (İbn Mâce, Ruhûn 4)",
    "Sizin en hayırlınız Kur'an'ı öğrenen ve öğretendir. (Buhârî, Fezâilü'l-Kur'ân 21)",
    "Kıskançlıktan sakının. Çünkü ateşin odunu yakıp tükettiği gibi, kıskançlık da iyi amelleri yakar, bitirir. (Ebû Dâvûd, Edeb 44)",
    "Bizi aldatan bizden değildir. (Müslim, Îmân 164)"
]; 
const day = Math.floor((new Date() - new Date(new Date().getFullYear(),0,0)) / 1000 / 60 / 60 / 24); 
const hadithElem = document.getElementById("daily-hadith");
if(hadithElem) hadithElem.innerText = hadiths[day % hadiths.length];
</script>"""

pattern = re.compile(r'<script>\s*const hadiths = \[\s*.*?\s*\];\s*const day = .*?(?:document\.getElementById\("daily-hadith"\)\.innerText = hadiths\[day % hadiths\.length\];|const hadithElem = document\.getElementById\("daily-hadith"\);\s*if\(hadithElem\)\s*hadithElem\.innerText = hadiths\[day % hadiths\.length\];)\s*</script>', re.DOTALL)

for root_dir, dirs, files in os.walk('.'):
    if '.git' in root_dir or '.vercel' in root_dir or '__pycache__' in root_dir:
        continue
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root_dir, file)
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            if 'const hadiths =' in content:
                new_content = pattern.sub(new_script, content)
                if new_content != content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    try:
                        print(f"Updated hadiths in {filepath}")
                    except UnicodeEncodeError:
                        print("Updated a file with special chars in name")
