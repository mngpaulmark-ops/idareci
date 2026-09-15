import re

with open('anasayfa.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# 1. Remove 404 scripts
content = re.sub(r'<script src="panel/tema/js/datepicker/js/jquery-ui-1.8.17.custom.min.js"></script>\n?', '', content)
content = re.sub(r'<script src="themes/burokratlar/tema/js/fancybox/fancybox/jquery.mousewheel-3.0.2.pack.js"[^>]*></script>\n?', '', content)

# 2. Remove broken event calendar init block
calendar_init_pattern = r'<script src="themes/burokratlar/tema/js/tasarim/etkinlik_takvimi/js/jquery.eventCalendar.js"></script>.*?monthNames: \[ "Ocak",.*?\}\);.*?</script>'
content = re.sub(calendar_init_pattern, '', content, flags=re.DOTALL)

# 3. Remove TRT Haber iframe
trt_pattern = r'<iframe frameborder="0" height="332" src="https://www.trthaber.com/sitene-ekle[^"]*" width="100%"></iframe>'
content = re.sub(trt_pattern, '<div style="padding:15px; text-align:center; color:#777; font-style:italic;">Haber akışı TRT Haber tarafından sonlandırıldığı için görüntülenemiyor.</div>', content)

with open('anasayfa.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("anasayfa.html cleaned of console errors!")
