import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_logic = """    turkey_areas = []
    world_areas = []
    list_html = ""
    
    for rep in reps:
        img_url = f"{rep.image_path}" if rep.image_path else "images/default-avatar.png"
        
        custom_data = f"<div style='text-align:center;'><img src='{img_url}' style='width:60px; height:60px; border-radius:50%; object-fit:cover; margin-bottom:5px;'><br><b>{rep.name}</b><br>{rep.phone or ''}</div>"
        
        area_obj = {
            "id": rep.city_code,
            "title": rep.city_name,
            "color": "rgba(0,201,181,0.8)",
            "customData": custom_data
        }
        
        if rep.city_code.startswith('TR-'):
            turkey_areas.append(area_obj)
        else:
            world_areas.append(area_obj)
        
        list_html += f'''
        <div class="col-12 col-md-6 col-lg-4" style="margin-bottom:20px; display:flex;">
            <div class="card border-0 shadow-sm" style="background:#fff; border-radius:10px; padding:15px; display:flex; flex-direction:row; align-items:center; width:100%; border: 1px solid #f1f1f1;">
                <img src="{img_url}" style="width:70px; height:70px; border-radius:50%; object-fit:cover; margin-right:15px; border:2px solid #eaeaea;" onerror="this.src='images/default-avatar.png'; this.onerror=null;">
                <div>
                    <h5 style="color:#800000; font-size:16px; font-weight:700; margin-bottom:5px;">{rep.name}</h5>
                    <div style="font-size:13px; color:#555; font-weight:500;">{rep.city_name} Temsilcisi</div>
                    <div style="font-size:13px; color:#777; margin-top:3px;"><i class="fa fa-phone"></i> {rep.phone or ''}</div>
                </div>
            </div>
        </div>
        '''"""

new_logic = """    turkey_areas = []
    world_areas_dict = {}
    
    import json
    try:
        with open('countries_tr.json', 'r', encoding='utf-8') as f:
            all_countries = json.load(f)
            for code, name in all_countries.items():
                world_areas_dict[code] = {
                    "id": code,
                    "title": name
                }
    except Exception:
        pass
        
    list_html = ""
    
    for rep in reps:
        img_url = f"{rep.image_path}" if rep.image_path else "images/default-avatar.png"
        
        custom_data = f"<div style='text-align:center;'><img src='{img_url}' style='width:60px; height:60px; border-radius:50%; object-fit:cover; margin-bottom:5px;'><br><b>{rep.name}</b><br>{rep.phone or ''}</div>"
        
        if rep.city_code.startswith('TR-'):
            turkey_areas.append({
                "id": rep.city_code,
                "title": rep.city_name,
                "color": "rgba(0,201,181,0.8)",
                "customData": custom_data
            })
        else:
            if rep.city_code in world_areas_dict:
                world_areas_dict[rep.city_code]["color"] = "rgba(0,201,181,0.8)"
                world_areas_dict[rep.city_code]["customData"] = custom_data
            else:
                world_areas_dict[rep.city_code] = {
                    "id": rep.city_code,
                    "title": rep.city_name,
                    "color": "rgba(0,201,181,0.8)",
                    "customData": custom_data
                }
        
        list_html += f'''
        <div class="col-12 col-md-6 col-lg-4" style="margin-bottom:20px; display:flex;">
            <div class="card border-0 shadow-sm" style="background:#fff; border-radius:10px; padding:15px; display:flex; flex-direction:row; align-items:center; width:100%; border: 1px solid #f1f1f1;">
                <img src="{img_url}" style="width:70px; height:70px; border-radius:50%; object-fit:cover; margin-right:15px; border:2px solid #eaeaea;" onerror="this.src='images/default-avatar.png'; this.onerror=null;">
                <div>
                    <h5 style="color:#800000; font-size:16px; font-weight:700; margin-bottom:5px;">{rep.name}</h5>
                    <div style="font-size:13px; color:#555; font-weight:500;">{rep.city_name} Temsilcisi</div>
                    <div style="font-size:13px; color:#777; margin-top:3px;"><i class="fa fa-phone"></i> {rep.phone or ''}</div>
                </div>
            </div>
        </div>
        '''
        
    world_areas = list(world_areas_dict.values())"""

new_content = content.replace(old_logic, new_logic)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Updated app.py")
