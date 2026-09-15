import re

with open('app.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('"zoomControl": {\n                        "zoomControlEnabled": true,\n                        "panControlEnabled": false,\n                        "homeButtonEnabled": true\n                    },',
'"zoomControl": {{\n                        "zoomControlEnabled": true,\n                        "panControlEnabled": false,\n                        "homeButtonEnabled": true\n                    }},')

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(text)
