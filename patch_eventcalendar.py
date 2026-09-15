import re

js_path = r'themes/burokratlar/tema/js/tasarim/etkinlik_takvimi/js/jquery.eventCalendar.js'

with open(js_path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Replace: flags.wrap.find('.eventsCalendar-day a').live('click',function(e){
# With:    flags.wrap.on('click', '.eventsCalendar-day a', function(e){
content = content.replace(
    "flags.wrap.find('.eventsCalendar-day a').live('click',function(e){",
    "flags.wrap.on('click', '.eventsCalendar-day a', function(e){"
)

content = content.replace(
    "flags.wrap.find('.monthTitle').live('click',function(e){",
    "flags.wrap.on('click', '.monthTitle', function(e){"
)

content = content.replace(
    "flags.wrap.find('.eventsCalendar-list .eventTitle').live('click',function(e){",
    "flags.wrap.on('click', '.eventsCalendar-list .eventTitle', function(e){"
)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("jquery.eventCalendar.js patched to use .on() instead of .live()")
