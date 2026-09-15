import re
with open('app.py', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

new = """'TR-80': 'Osmaniye',
    'TR-81': 'Düzce',
    'AZ': 'Azerbaycan', 'DE': 'Almanya', 'US': 'Amerika Birleşik Devletleri',
    'FR': 'Fransa', 'GB': 'İngiltere', 'NL': 'Hollanda', 'BE': 'Belçika',
    'AT': 'Avusturya', 'CH': 'İsviçre', 'IT': 'İtalya', 'RU': 'Rusya',
    'KZ': 'Kazakistan', 'UZ': 'Özbekistan', 'TM': 'Türkmenistan', 'KG': 'Kırgızistan',
    'CY': 'Kuzey Kıbrıs (KKTC)', 'BA': 'Bosna Hersek', 'MK': 'Makedonya',
    'AL': 'Arnavutluk', 'XK': 'Kosova', 'BG': 'Bulgaristan', 'GR': 'Yunanistan',
    'IQ': 'Irak', 'SY': 'Suriye', 'IR': 'İran', 'SA': 'Suudi Arabistan',
    'QA': 'Katar', 'AE': 'Birleşik Arap Emirlikleri', 'EG': 'Mısır', 'PK': 'Pakistan',
    'AF': 'Afganistan', 'IN': 'Hindistan', 'CN': 'Çin', 'JP': 'Japonya',
    'KR': 'Güney Kore', 'AU': 'Avustralya', 'CA': 'Kanada', 'BR': 'Brezilya',
    'ZA': 'Güney Afrika'"""

text = re.sub(r"'TR-80': 'Osmaniye',\s*'TR-81': '[^']+'", new, text)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(text)
print("Updated CITIES")
