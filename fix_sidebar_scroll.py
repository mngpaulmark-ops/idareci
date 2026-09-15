import re

with open('themes/burokratlar/tema/css/style.css', 'r', encoding='utf-8') as f:
    content = f.read()

# I added this block:
# /* Sticky Sidebar CSS */
# #left {
#     position: -webkit-sticky;
#     position: sticky;
#     top: 15px;
#     max-height: calc(100vh - 30px);
#     overflow-y: auto;
#     /* Optional: Hide scrollbar for cleaner look but keep functionality */
#     scrollbar-width: thin;
#     scrollbar-color: #800000 transparent;
# }
# #left::-webkit-scrollbar {
#     width: 6px;
# }
# #left::-webkit-scrollbar-thumb {
#     background-color: #800000;
#     border-radius: 3px;
# }

# I will replace it with a simpler one that has NO scrollbar and NO max-height.
# It will just be:
# /* Sticky Sidebar CSS */
# #left {
#     position: -webkit-sticky;
#     position: sticky;
#     top: 15px;
# }

pattern = r'/\* Sticky Sidebar CSS \*/.*?border-radius: 3px;\s*\}'
replacement = '''/* Sticky Sidebar CSS */
#left {
    position: -webkit-sticky;
    position: sticky;
    top: 15px;
}'''

new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open('themes/burokratlar/tema/css/style.css', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Updated style.css to remove max-height and scrollbar from sticky sidebar.")
