import os
import re

fb_html = '''<div class="fb-page" data-href="https://www.facebook.com/Burokratlarbirligi-327956840549801/" data-tabs="timeline" data-width="100%" data-height="332" data-small-header="true" data-adapt-container-width="true" data-hide-cover="false" data-show-facepile="false"><blockquote cite="https://www.facebook.com/Burokratlarbirligi-327956840549801/" class="fb-xfbml-parse-ignore"><a href="https://www.facebook.com/Burokratlarbirligi-327956840549801/">İdareci ve Bürokratlar Birliği Derneği</a></blockquote></div>'''

trt_html = '''<div id="trt-widget" style="height: 332px; overflow-y: auto; background: #fff; padding: 10px; border: 1px solid #ddd;">
    <div style="text-align:center;"><img src="/themes/burokratlar/tema/images/icon-trt.png" width="30" /> Yükleniyor...</div>
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
</script>'''

for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith(('.html', '.htm', '.php', '.tpl')):
            path = os.path.join(root, file)
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                changed = False
                
                # Fix Facebook
                if 'fb-root' in content and 'fb-page' not in content:
                    content = re.sub(r'(facebook-jssdk\'\)\);\s*</script>)', r'\1\n' + fb_html, content)
                    changed = True
                    
                # Fix facebook script src protocol
                if 'js.src = "//connect.facebook.net' in content:
                    content = content.replace('js.src = "//connect.facebook.net', 'js.src = "https://connect.facebook.net')
                    changed = True
                    
                # Fix TRT
                if 'trthaber.com/sitene-ekle' in content:
                    content = re.sub(r'<iframe[^>]*?trthaber[^>]*?>.*?</iframe>', trt_html, content, flags=re.DOTALL)
                    changed = True
                    
                if changed:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f'Fixed widgets in {path}')
            except Exception as e:
                pass
print('Done fixing widgets globally')
