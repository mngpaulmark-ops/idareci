import re

with open('update_anasayfa.py', 'r', encoding='utf-8') as f:
    c = f.read()

pattern = r"list_group\['style'\] =.*?for h in latest\[:5\]:"

replacement = """list_group['style'] = "height: 332px; overflow-y: auto; overflow-x: hidden; padding-right: 5px;" 
                    
                    # Remove any extra list-group divs that might be left over from the original template
                    panel_body = news_panel.find('div', class_='col-md-6').find('div', class_='panel-body')
                    if panel_body:
                        extra_groups = panel_body.find_all('div', class_='list-group')
                        for eg in extra_groups[1:]:
                            eg.decompose()
                            
                    for h in latest[:5]:"""

new_c = re.sub(pattern, replacement, c, flags=re.DOTALL)

with open('update_anasayfa.py', 'w', encoding='utf-8') as f:
    f.write(new_c)

print("Forced update update_anasayfa.py")
