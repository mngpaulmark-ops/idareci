import re

with open('themes/burokratlar/tema/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# The target block is:
"""
@media (max-width: 1000px) {
.basin {
    display:none !important;
}
.icon {
    display: block;
    bottom:7px;
    left:-5px;
}
.left-menu {
    z-index: 1000;
    position: absolute;
    background-color: #ffffff;
    margin-left: -400px;
}
}
"""

# We want to replace it with:
"""
@media (max-width: 1000px) {
.basin {
    display:none !important;
}
.icon {
    display: none !important;
}
.left-menu {
    display: none !important;
}
}
"""

pattern = re.compile(r'@media \(max-width: 1000px\) \{.*?\.basin \{.*?display:none !important;.*?\}\s*\.icon \{.*?\}\s*\.left-menu \{.*?margin-left: -400px;.*?\}\s*\}', re.DOTALL)

def replacer(match):
    return """@media (max-width: 1000px) {
.basin {
    display:none !important;
}
.icon {
    display: none !important;
}
.left-menu {
    display: none !important;
}
#left {
    display: none !important;
}
}"""

new_css = re.sub(pattern, replacer, css)

if new_css != css:
    with open('themes/burokratlar/tema/css/style.css', 'w', encoding='utf-8') as f:
        f.write(new_css)
    print("Fixed mobile menu CSS!")
else:
    print("Could not find the block to replace!")
