import bs4
import glob
import re

# 1. Update anasayfa.html to equalize heights
with open('anasayfa.html', 'r', encoding='utf-8') as f:
    content = f.read()

soup = bs4.BeautifulSoup(content, 'lxml')

# Find the row containing the widgets
panel_kamu = soup.find('div', id='panel-kamu-etigi')
if panel_kamu:
    parent_col1 = panel_kamu.parent
    parent_row = parent_col1.parent
    
    # Make the row a flexbox to equalize heights
    parent_row['style'] = parent_row.get('style', '') + ' display: flex; flex-wrap: wrap;'
    
    # Make both panels stretch to full height
    panel_kamu['style'] = panel_kamu.get('style', '') + ' height: 100%; display: flex; flex-direction: column;'
    
    panel_yonetim = soup.find('div', id='panel-yonetim-liderlik')
    if panel_yonetim:
        panel_yonetim['style'] = panel_yonetim.get('style', '') + ' height: 100%; display: flex; flex-direction: column;'
        
        # Also make their body containers flex-grow to push buttons to bottom
        kamu_body = panel_kamu.find('div', class_='panel-body')
        if kamu_body:
            kamu_body['style'] = kamu_body.get('style', '') + ' flex-grow: 1; display: flex; flex-direction: column;'
            inner_div = kamu_body.find('div')
            if inner_div:
                inner_div['style'] = inner_div.get('style', '') + ' flex-grow: 1; display: flex; flex-direction: column; justify-content: space-between;'
                
        yonetim_body = panel_yonetim.find('div', class_='panel-body')
        if yonetim_body:
            yonetim_body['style'] = yonetim_body.get('style', '') + ' flex-grow: 1; display: flex; flex-direction: column;'
            inner_div2 = yonetim_body.find('div')
            if inner_div2:
                inner_div2['style'] = inner_div2.get('style', '') + ' flex-grow: 1; display: flex; flex-direction: column; justify-content: space-between;'

    with open('anasayfa.html', 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print("Fixed anasayfa.html heights.")

