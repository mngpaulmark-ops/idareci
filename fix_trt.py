import re

html_code = '''
<div id="trt-widget" style="height: 332px; overflow-y: auto; background: #fff; padding: 10px; border: 1px solid #ddd;">
    <div style="text-align:center;"><img src="themes/burokratlar/tema/images/icon-trt.png" width="30" /> Yükleniyor...</div>
</div>
<script>
fetch('https://api.rss2json.com/v1/api.json?rss_url=https%3A%2F%2Fwww.trthaber.com%2Fxml_mobile.php%3Ftur%3Dxml_genel')
  .then(function(response) { return response.json(); })
  .then(function(data) {
    var container = document.getElementById('trt-widget');
    container.innerHTML = '';
    if (data.items) {
        data.items.slice(0, 10).forEach(function(item) {
            container.innerHTML += '<div style="margin-bottom: 10px; border-bottom: 1px solid #eee; padding-bottom: 5px;">' +
                '<a href="' + item.link + '" target="_blank" style="text-decoration: none; color: #333; font-weight: bold; font-size: 13px;">' +
                item.title + '</a></div>';
        });
    } else {
        container.innerHTML = 'Haberler yüklenemedi.';
    }
  }).catch(function(err) {
      document.getElementById('trt-widget').innerHTML = 'Haberler yüklenemedi.';
  });
</script>
'''

with open('anasayfa.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = re.sub(r'<iframe[^>]*?trthaber[^>]*?>.*?</iframe>', html_code, text, flags=re.DOTALL)

with open('anasayfa.html', 'w', encoding='utf-8') as f:
    f.write(text)
print('TRT fixed')
