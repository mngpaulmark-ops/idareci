import re

with open('update_map.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Add zoomControl and maintainAspectRatio to commonSettings
pattern = re.compile(r'"backgroundColor": "rgba\(255,255,255,1\)",', re.DOTALL)
replacement = """"backgroundColor": "rgba(255,255,255,1)",
                    "zoomControl": {
                        "zoomControlEnabled": true,
                        "panControlEnabled": false,
                        "homeButtonEnabled": true
                    },
                    "maintainAspectRatio": true,"""

new_code = re.sub(pattern, replacement, code)

with open('update_map.py', 'w', encoding='utf-8') as f:
    f.write(new_code)
