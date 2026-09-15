import re

with open('update_map.py', 'r', encoding='utf-8') as f:
    code = f.read()

pattern = re.compile(r'"map": "turkeyLow",\s*"getAreasFromMap": true,\s*"areas": \{turkey_json\}')
replacement = """"map": "turkeyLow",
                "getAreasFromMap": true,
                "zoomLevel": 0.9,
                "zoomLongitude": 35.5,
                "zoomLatitude": 39.0,
                "areas": {turkey_json}"""

new_code = re.sub(pattern, replacement, code)

with open('update_map.py', 'w', encoding='utf-8') as f:
    f.write(new_code)
