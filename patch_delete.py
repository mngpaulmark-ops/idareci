import re

with open('app.py', 'r', encoding='utf-8') as f:
    text = f.read()

# For admin_kose_sil
if "yazar_id = yazi.yazar_id" not in text:
    text = re.sub(
        r'(def admin_kose_sil\(id\):.*?yazi = KoseYazisi.*?get_or_404\(id\)\n)', 
        r'\g<1>    yazar_id = yazi.yazar_id\n', 
        text, 
        flags=re.DOTALL
    )
    text = text.replace(
        "db.session.delete(yazi)\n    db.session.commit()\n    return redirect(url_for('admin_kose_list'))", 
        "db.session.delete(yazi)\n    db.session.commit()\n    kose_helper.regenerate_single_yazar(yazar_id)\n    import os\n    if os.path.exists(f'kose-yazilari-{id}.html'): os.remove(f'kose-yazilari-{id}.html')\n    return redirect(url_for('admin_kose_list'))"
    )

    # For yazar_panel_sil
    text = re.sub(
        r'(def yazar_panel_sil\(id\):.*?yazi = KoseYazisi.*?get_or_404\(id\)\n)', 
        r'\g<1>    yazar_id = yazi.yazar_id\n', 
        text, 
        flags=re.DOTALL
    )
    text = text.replace(
        "db.session.delete(yazi)\n    db.session.commit()\n    return redirect(url_for('yazar_panel'))", 
        "db.session.delete(yazi)\n    db.session.commit()\n    kose_helper.regenerate_single_yazar(yazar_id)\n    import os\n    if os.path.exists(f'kose-yazilari-{id}.html'): os.remove(f'kose-yazilari-{id}.html')\n    return redirect(url_for('yazar_panel'))"
    )

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(text)
