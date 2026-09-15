import re
with open('anasayfa.html', 'r', encoding='utf-8') as f:
    text = f.read()

fb_html = '<div class="fb-page" data-href="https://www.facebook.com/Burokratlarbirligi-327956840549801/" data-tabs="timeline" data-width="100%" data-height="332" data-small-header="true" data-adapt-container-width="true" data-hide-cover="false" data-show-facepile="false"><blockquote cite="https://www.facebook.com/Burokratlarbirligi-327956840549801/" class="fb-xfbml-parse-ignore"><a href="https://www.facebook.com/Burokratlarbirligi-327956840549801/">İdareci ve Bürokratlar Birliği Derneği</a></blockquote></div>'

text = re.sub(r"(facebook-jssdk'\)\);\s*</script>)", r"\1\n" + fb_html, text)

with open('anasayfa.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Facebook fixed")
