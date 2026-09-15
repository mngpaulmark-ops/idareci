import re

with open('themes/burokratlar/tema/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# We want to replace the block I just added in the previous step:
pattern = re.compile(r'@media \(max-width: 1000px\) \{\s*\.basin \{\s*display:none !important;\s*\}\s*\.icon \{\s*display: none !important;\s*\}\s*\.left-menu \{\s*display: none !important;\s*\}\s*#left \{\s*display: none !important;\s*\}\s*\}', re.DOTALL)

def replacer(match):
    return """@media (max-width: 1000px) {
.basin {
    display:none !important;
}
.icon {
    display: block !important;
    bottom:7px;
    left:-5px;
    cursor: pointer;
}
.left-menu {
    display: none;
    position: static !important;
    margin-left: 0 !important;
    width: 100% !important;
    background-color: transparent !important;
    padding: 0 !important;
}
#left {
    display: block !important;
    margin-bottom: 15px;
}
}"""

new_css = re.sub(pattern, replacer, css)

if new_css != css:
    with open('themes/burokratlar/tema/css/style.css', 'w', encoding='utf-8') as f:
        f.write(new_css)
    print("Fixed style.css for slideToggle left menu!")
else:
    print("Could not find the block to replace in style.css!")
