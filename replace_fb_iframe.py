import re

with open('anasayfa.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the iframe with a styled link block
new_html = '''
<div style="background-color: #f0f2f5; border: 1px solid #ddd; border-radius: 8px; padding: 20px; text-align: center; margin-top: 10px;">
    <img src="themes/burokratlar/tema/images/icon-facebook.png" style="width: 50px; margin-bottom: 15px;" alt="Facebook" />
    <h4 style="color: #1877f2; font-weight: bold; margin-bottom: 10px;">İdareci ve Bürokratlar Birliği</h4>
    <p style="color: #65676b; font-size: 13px; margin-bottom: 20px;">Facebook üzerinden bizi takip edin ve güncel etkinliklerimizden anında haberdar olun.</p>
    <a href="https://www.facebook.com/people/Burokratlarbirligi/100064380711410/" target="_blank" style="display: inline-block; background-color: #1877f2; color: white; padding: 8px 20px; border-radius: 6px; text-decoration: none; font-weight: bold; font-size: 14px;">Facebook Profiline Git</a>
</div>
'''

# The current iframe has:
# <iframe src="https://www.facebook.com/plugins/page.php?href=https%3A%2F%2Fwww.facebook.com%2Fpeople%2FBurokratlarbirligi%2F100064380711410%2F&tabs=timeline&width=340&height=332&small_header=true&adapt_container_width=true&hide_cover=false&show_facepile=false&appId=210306796005157" width="100%" height="332" style="border:none;overflow:hidden" scrolling="no" frameborder="0" allowfullscreen="true" allow="autoplay; clipboard-write; encrypted-media; picture-in-picture; web-share"></iframe>

pattern = r'<iframe src="https://www\.facebook\.com/plugins/page\.php\?href=https%3A%2F%2Fwww\.facebook\.com%2Fpeople%2FBurokratlarbirligi.*?></iframe>'

new_content = re.sub(pattern, new_html, content, flags=re.DOTALL)

with open('anasayfa.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Replaced broken iframe with styled direct link widget.")
