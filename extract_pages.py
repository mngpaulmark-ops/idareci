import os, bs4, re

sql_path = r'C:\Users\turga\OneDrive\Desktop\bürokratlar birliği orjinal site yedeği\backup-8.11.2026_11-19-03_burokratlarbirli\backup-8.11.2026_11-19-03_burokratlarbirli\mysql\burokratlarbirli_database.sql'
sql = open(sql_path, encoding='utf-8', errors='ignore').read()

slugs = ['tuzugumuz', 'yonetimkurulu', 'baskanlik-ve-birimler', 'yuksek-istisare-onur-kurulu-uyesi', 'diger-kurullar', 'temsilcilik']
for slug in slugs:
    # Match the row in the VALUES clause
    # ... ,'slug','<content>','1'),( ...
    pattern = rf"'{slug}','(.*?)','\d'\)"
    match = re.search(pattern, sql)
    if match:
        html_content = match.group(1)
        
        # Unescape MySQL string (naive)
        html_content = html_content.replace('\\\'', '\'')
        html_content = html_content.replace('\\r\\n', '\n')
        html_content = html_content.replace('\\n', '\n')
        html_content = html_content.replace('\\"', '"')
        
        filename = f'{slug}.html'
        if os.path.exists(filename):
            try:
                f_html = open(filename, encoding='utf-8', errors='ignore').read()
                soup = bs4.BeautifulSoup(f_html, 'lxml')
                panels = soup.find_all('div', class_='panel-body')
                if panels:
                    content_div = panels[-1]
                    box = content_div.find('div', class_='box')
                    new_content = bs4.BeautifulSoup(html_content, 'html.parser')
                    if box:
                        box.clear()
                        box.append(new_content)
                    else:
                        content_div.clear()
                        content_div.append(new_content)
                        
                    open(filename, 'w', encoding='utf-8').write(str(soup))
                    print(f'Updated {filename}')
            except Exception as e:
                print('Error on', filename, e)

print('Done extracting missing content.')
