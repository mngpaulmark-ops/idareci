import re

with open('anasayfa.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# The event calendar HTML
event_cal_html = """
<div class="panel panel-primary" style="margin-top:20px;">
    <div class="panel-heading"><img src="themes/burokratlar/tema/images/icon-announce.png" alt=""/> Etkinlik Takvimi</div>
    <div class="panel-body">
        <div id="eventCalendarLocale"></div>
    </div>
</div>
"""

# Find where to inject it. Let's put it right after the kayan_alan (yazarlar) widget.
# </ul>\n</div></div>\n<div class="clearfix"></div>\n<div class="news">
target_pattern = r'(</ul>\s*</div></div>)\s*<div class="clearfix"></div>\s*<div class="news">'

# Wait, in the HTML it's:
# </ul>
# </div></div>
# <div class="clearfix"></div>
# <div class="news">

if 'id="eventCalendarLocale"' not in content:
    content = re.sub(target_pattern, r'\1\n' + event_cal_html + r'\n<div class="clearfix"></div>\n<div class="news">', content)
    
    # Also inject the JS scripts at the end before </body>
    js_scripts = """
<script src="themes/burokratlar/tema/js/tasarim/etkinlik_takvimi/js/jquery.eventCalendar.js"></script>
<link href="themes/burokratlar/tema/js/tasarim/etkinlik_takvimi/css/eventCalendar.css" rel="stylesheet" />
<link href="themes/burokratlar/tema/js/tasarim/etkinlik_takvimi/css/eventCalendar_theme_responsive.css" rel="stylesheet" />
<script type="text/javascript">
    $(document).ready(function() {
        var eventsInline = []; // This will be populated by etkinlik_helper.py
        $("#eventCalendarLocale").eventCalendar({
            jsonData: eventsInline,
            cacheJson: false,
            showDescription: true,
            eventsLimit: 5,
            monthNames: [ "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık" ],
            dayNames: [ 'Pazar','Pazartesi','Salı','Çarşamba', 'Perşembe','Cuma','Cumartesi' ],
            dayNamesShort: [ 'Paz','Pzt','Sal','Çar', 'Per','Cum','Cmt' ],
            txt_noEvents: "Bu ay için etkinlik bulunamadı.",
            txt_SpecificEvents_prev: "",
            txt_SpecificEvents_after: " Etkinlikleri:",
            txt_next: "Sonraki",
            txt_prev: "Önceki",
            txt_NextEvents: "Yaklaşan Etkinlikler:",
            txt_GoToEventUrl: "Detaylı Görüntüle"
        });
    });
</script>
"""
    content = content.replace('</body>', js_scripts + '\n</body>')
    with open('anasayfa.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Event calendar HTML and JS injected into anasayfa.html")
else:
    print("Event calendar already in anasayfa.html")
