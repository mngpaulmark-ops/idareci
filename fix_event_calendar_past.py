import re

js_path = 'themes/burokratlar/tema/js/tasarim/etkinlik_takvimi/js/jquery.eventCalendar.js'

with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Disable the filter that hides past events on initial load
content = content.replace(
    'if (month === false && eventDate < new Date()) {',
    'if (false) { // Disabled past event filter'
)

# Also, if we sort by date ascending, past events will be at the very top (e.g. from 2016).
# The user wants to see the most recent ones if they are in the past.
# Actually, eventCalendar limits to `eventsLimit` (which is 5).
# If we sort them ascending, we'll get the 5 OLDEST events.
# Let's change the sortJson function to sort DESCENDING so we get the most recent ones!
# Sort function is: 
# function sortJson(a, b){ return a.date.toLowerCase() > b.date.toLowerCase() ? 1 : -1; }
content = content.replace(
    'return a.date.toLowerCase() > b.date.toLowerCase() ? 1 : -1;',
    'return parseInt(a.date) < parseInt(b.date) ? 1 : -1;'
)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("jquery.eventCalendar.js modified to show most recent past events!")
