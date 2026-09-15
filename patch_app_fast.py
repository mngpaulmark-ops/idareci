with open('app.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# Insert import at the top
if 'import kose_helper' not in text:
    text = text.replace('import os', 'import os\nimport kose_helper')

# For admin_kose_ekle
old1 = "db.session.add(yeni_yazi)\n    db.session.commit()\n    os.system('python generate_kose.py')\n    os.system('python generate_kose_yazarlari.py')\n    return redirect(url_for('admin_kose_list'))"
new1 = "db.session.add(yeni_yazi)\n    db.session.commit()\n    kose_helper.regenerate_single_kose(yeni_yazi.id)\n    kose_helper.regenerate_single_yazar(yeni_yazi.yazar_id)\n    return redirect(url_for('admin_kose_list'))"
text = text.replace(old1, new1)

# For yazar_panel_ekle
old2 = "db.session.add(yeni_yazi)\n    db.session.commit()\n    os.system('python generate_kose.py')\n    os.system('python generate_kose_yazarlari.py')\n    return redirect(url_for('yazar_panel'))"
new2 = "db.session.add(yeni_yazi)\n    db.session.commit()\n    kose_helper.regenerate_single_kose(yeni_yazi.id)\n    kose_helper.regenerate_single_yazar(yeni_yazi.yazar_id)\n    return redirect(url_for('yazar_panel'))"
text = text.replace(old2, new2)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(text)
