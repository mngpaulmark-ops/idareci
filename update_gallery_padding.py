import re

with open('themes/burokratlar/tema/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# I will replace the previous gallery styles block
old_block = """/* Custom Gallery Styles for Uniform Images */
.fotogaleri.jcarousel ul li img,
.videogaleri.jcarousel ul li img {
    height: 130px !important;
    width: 100% !important;
    object-fit: cover !important;
    border-radius: 4px;
}"""

new_block = """/* Custom Gallery Styles for Uniform Images */
.fotogaleri.jcarousel ul li a.center-image,
.videogaleri.jcarousel ul li a.center-image {
    display: block;
    padding-left: 8px;
    padding-right: 8px;
}
.fotogaleri.jcarousel ul li img,
.videogaleri.jcarousel ul li img {
    height: 130px !important;
    width: 100% !important;
    object-fit: cover !important;
    border-radius: 4px;
}"""

if old_block in css:
    css = css.replace(old_block, new_block)
else:
    # If slight formatting differences, use regex
    css = re.sub(r'/\* Custom Gallery Styles for Uniform Images \*/.*?(?=\n\n|\Z)', new_block, css, flags=re.DOTALL)

with open('themes/burokratlar/tema/css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Gallery CSS updated with padding.")
