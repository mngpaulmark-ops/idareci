with open('templates/admin/haber_edit.html', 'r', encoding='utf-8') as f:
    text = f.read()

new_field = '''
            <div class="mb-3">
                <label class="form-label">Tarih</label>
                <input type="date" name="date" class="form-control" value="{{ haber.date.strftime('%Y-%m-%d') if haber and haber.date else '' }}" required>
            </div>
            <div class="mb-3">
'''
text = text.replace('<div class="mb-3">', new_field, 1)

with open('templates/admin/haber_edit.html', 'w', encoding='utf-8') as f:
    f.write(text)
print('Updated haber_edit.html')
