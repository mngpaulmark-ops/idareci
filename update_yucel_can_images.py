import re

with open('generate_kose.py', 'r', encoding='utf-8') as f:
    content = f.read()

# We need to conditionalize the small author block and adjust the banner size

pattern = re.compile(r'(<div style="float: left; margin-right: 15px; margin-bottom: 15px; text-align: center;">\s*<a href="kose-yazar-\{yazar_id\}\.html">\s*<img src="\{yazar_pic\}" style="max-width: 150px;"/>\s*<br/><b>\{yazar_name\}</b>\s*</a>\s*</div>)', re.DOTALL)

replacement = """{'''<div style="float: left; margin-right: 15px; margin-bottom: 15px; text-align: center;">
                                <a href="kose-yazar-{yazar_id}.html">
                                    <img src="{yazar_pic}" style="max-width: 150px;"/>
                                    <br/><b>{yazar_name}</b>
                                </a>
                            </div>''' if str(yazar_id) != '1' else ''}"""

content = re.sub(pattern, replacement, content)

# Now adjust the banner
banner_pattern = re.compile(r"width:100%; max-width:100%; border-radius:8px; margin-bottom:20px; box-shadow: 0 4px 8px rgba\(0,0,0,0\.1\);")
banner_replacement = "width:100%; max-width:600px; display:block; margin: 0 auto 20px auto; border-radius:8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);"

content = re.sub(banner_pattern, banner_replacement, content)

with open('generate_kose.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated generate_kose.py!")
