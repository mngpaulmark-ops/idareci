import re

with open('update_anasayfa.py', 'r', encoding='utf-8') as f:
    c = f.read()

old_block = """                if list_group:
                    list_group.clear()"""

new_block = """                if list_group:
                    list_group.clear()
                    list_group['style'] = "height: 332px; overflow-y: auto; overflow-x: hidden; padding-right: 5px;" """

if old_block in c:
    c = c.replace(old_block, new_block)
    with open('update_anasayfa.py', 'w', encoding='utf-8') as f:
        f.write(c)
    print("Updated update_anasayfa.py")
else:
    print("Could not find block.")
