with open('app.py', 'r', encoding='utf-8') as f:
    text = f.read()

old_area = '''        area_obj = {
            "id": rep.city_code,
            "title": rep.city_name,
            "color": "rgba(0,201,181,0.8)",
            "customData": custom_data
        }'''
new_area = '''        area_obj = {
            "id": rep.city_code,
            "title": rep.city_name,
            "color": "rgba(0,201,181,0.8)",
            "balloonText": f"<div style='font-size:14px;'><b>{rep.city_name}</b></div><div style='margin-top:5px;'>{custom_data}</div>"
        }'''
text = text.replace(old_area, new_area)

old_balloon = '''"balloonText": "<div style='font-size:14px;'><b>[[title]]</b></div><div style='margin-top:5px;'>[[customData]]</div>",'''
new_balloon = '''"balloonText": "",'''
text = text.replace(old_balloon, new_balloon)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(text)
