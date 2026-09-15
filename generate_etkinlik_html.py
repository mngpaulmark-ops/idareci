import re

sql_path = r"C:\Users\turga\OneDrive\Desktop\bürokratlar birliği orjinal site yedeği\backup-8.11.2026_11-19-03_burokratlarbirli\backup-8.11.2026_11-19-03_burokratlarbirli\homedir\public_html\SQL YEDEK\burokrat_database.sql"
with open(sql_path, 'r', encoding='utf-8', errors='ignore') as f:
    sql = f.read()

# Find the INSERT for etkinlik
match = re.search(r"INSERT INTO `burokratlar_etkinlik` VALUES (.*?);", sql)
if match:
    values_str = match.group(1)
    # Poor man's tuple parser
    values = re.findall(r"\((.*?)\)", values_str)
    
    html = "<h3>Geçmiş Etkinliklerimiz</h3><hr/>"
    for v in values:
        parts = v.split("','")
        if len(parts) >= 8:
            title = parts[4]
            desc = parts[5]
            loc = parts[8]
            time = parts[9].replace("'", "")
            html += f"<div style='margin-bottom: 20px; padding: 15px; border: 1px solid #ddd; border-radius: 5px;'>"
            html += f"<h4 style='color: #800000; margin-top: 0;'>{title}</h4>"
            html += f"<p><strong>Saat:</strong> {time} | <strong>Yer:</strong> {loc}</p>"
            html += f"<p>{desc}</p>"
            html += f"</div>"
            
    print("Generated HTML for etkinlik:")
    print(html[:200])
    
    # Save it to DB
    import sqlite3
    conn = sqlite3.connect('instance/cms.db')
    c = conn.cursor()
    c.execute('UPDATE page SET content_html=? WHERE slug=?', (html, 'etkinlik'))
    conn.commit()
    conn.close()
    print("Updated cms.db!")
else:
    print("Etkinlik insert not found in SQL.")
