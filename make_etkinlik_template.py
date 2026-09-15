import re
import os

with open('etkinlikler.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

jinja2_code = """
<div class="main">
    <div class="title">
        <img src="themes/burokratlar/tema/images/icon-announce.png" alt=""> ETKİNLİKLER
    </div>
    
    <div class="list-group" style="margin-top:20px;">
    {% for e in etkinlikler %}
        <div class="list-group-item" style="margin-bottom:15px; padding:15px; border:1px solid #ddd; border-radius:5px; border-left:5px solid #800000;">
            <h4 style="color:#800000; margin-top:0; font-weight:bold;">{{ e.title }}</h4>
            <div style="font-size:12px; color:#666; margin-bottom:10px;">
                <i class="fa fa-calendar"></i> {{ e.edate }} 
                {% if e.saat %}<i class="fa fa-clock-o" style="margin-left:10px;"></i> {{ e.saat }}{% endif %}
            </div>
            <p style="font-size:14px; line-height:1.6; color:#333;">{{ e.description|safe }}</p>
            {% if e.link and e.link != '#' %}
            <a href="{{ e.link }}" class="btn btn-sm btn-primary" style="background-color:#0f2b48; border:none; margin-top:10px;">Detaylar</a>
            {% endif %}
        </div>
    {% else %}
        <div class="alert alert-warning">Şu anda kayıtlı bir etkinlik bulunmamaktadır.</div>
    {% endfor %}
    </div>
</div>
"""

# Replace the content of <div class="main">...</div>
# First find <div class="col-md-9" id="main">\n  <div class="main">
pattern = r'<div class="main">.*?</div> </div>'
# Wait, the structure in the file is:
# <div class="col-md-9" id="main">
#  <div class="main">
#   ...
#  </div> </div>

# Let's just do a simpler replace.
main_pattern = r'<div class="main">.*?(?=</div>\s*</div>\s*</div>\s*</div>\s*<footer)'

content = re.sub(main_pattern, jinja2_code, content, flags=re.DOTALL)

with open('templates/etkinlik_page.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.remove('etkinlikler.html')
print("Created templates/etkinlik_page.html and deleted static etkinlikler.html")
