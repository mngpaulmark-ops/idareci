import re

css_inject = """
/* Sticky Sidebar CSS */
#left {
    position: -webkit-sticky;
    position: sticky;
    top: 15px;
    max-height: calc(100vh - 30px);
    overflow-y: auto;
    /* Optional: Hide scrollbar for cleaner look but keep functionality */
    scrollbar-width: thin;
    scrollbar-color: #800000 transparent;
}
#left::-webkit-scrollbar {
    width: 6px;
}
#left::-webkit-scrollbar-thumb {
    background-color: #800000;
    border-radius: 3px;
}
"""

with open('themes/burokratlar/tema/css/style.css', 'a', encoding='utf-8') as f:
    f.write('\n' + css_inject)

print("Injected sticky sidebar CSS into style.css")
