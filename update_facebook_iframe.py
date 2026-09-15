import re

with open('anasayfa.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the entire Facebook SDK block with an iframe
iframe_html = '''<iframe src="https://www.facebook.com/plugins/page.php?href=https%3A%2F%2Fwww.facebook.com%2Fpeople%2FBurokratlarbirligi%2F100064380711410%2F&tabs=timeline&width=340&height=332&small_header=true&adapt_container_width=true&hide_cover=false&show_facepile=false&appId=210306796005157" width="100%" height="332" style="border:none;overflow:hidden" scrolling="no" frameborder="0" allowfullscreen="true" allow="autoplay; clipboard-write; encrypted-media; picture-in-picture; web-share"></iframe>'''

# Pattern to match the existing fb-root and fb-page
pattern = r'<div id="fb-root"></div>\s*<script>.*?facebook-jssdk\'\)\);</script>\s*<div class="fb-page".*?</div>'

new_content = re.sub(pattern, iframe_html, content, flags=re.DOTALL)

with open('anasayfa.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Facebook widget replaced with iframe.")
