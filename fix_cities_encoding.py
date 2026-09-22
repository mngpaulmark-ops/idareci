import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

correct_cities = """CITIES = {
    'TR-01': 'Adana', 'TR-02': 'Adıyaman', 'TR-03': 'Afyonkarahisar', 'TR-04': 'Ağrı', 'TR-05': 'Amasya',
    'TR-06': 'Ankara', 'TR-07': 'Antalya', 'TR-08': 'Artvin', 'TR-09': 'Aydın', 'TR-10': 'Balıkesir',
    'TR-11': 'Bilecik', 'TR-12': 'Bingöl', 'TR-13': 'Bitlis', 'TR-14': 'Bolu', 'TR-15': 'Burdur',
    'TR-16': 'Bursa', 'TR-17': 'Çanakkale', 'TR-18': 'Çankırı', 'TR-19': 'Çorum', 'TR-20': 'Denizli',
    'TR-21': 'Diyarbakır', 'TR-22': 'Edirne', 'TR-23': 'Elazığ', 'TR-24': 'Erzincan', 'TR-25': 'Erzurum',
    'TR-26': 'Eskişehir', 'TR-27': 'Gaziantep', 'TR-28': 'Giresun', 'TR-29': 'Gümüşhane', 'TR-30': 'Hakkari',
    'TR-31': 'Hatay', 'TR-32': 'Isparta', 'TR-33': 'Mersin', 'TR-34': 'İstanbul', 'TR-35': 'İzmir',
    'TR-36': 'Kars', 'TR-37': 'Kastamonu', 'TR-38': 'Kayseri', 'TR-39': 'Kırklareli', 'TR-40': 'Kırşehir',
    'TR-41': 'Kocaeli', 'TR-42': 'Konya', 'TR-43': 'Kütahya', 'TR-44': 'Malatya', 'TR-45': 'Manisa',
    'TR-46': 'Kahramanmaraş', 'TR-47': 'Mardin', 'TR-48': 'Muğla', 'TR-49': 'Muş', 'TR-50': 'Nevşehir',
    'TR-51': 'Niğde', 'TR-52': 'Ordu', 'TR-53': 'Rize', 'TR-54': 'Sakarya', 'TR-55': 'Samsun',
    'TR-56': 'Siirt', 'TR-57': 'Sinop', 'TR-58': 'Sivas', 'TR-59': 'Tekirdağ', 'TR-60': 'Tokat',
    'TR-61': 'Trabzon', 'TR-62': 'Tunceli', 'TR-63': 'Şanlıurfa', 'TR-64': 'Uşak', 'TR-65': 'Van',
    'TR-66': 'Yozgat', 'TR-67': 'Zonguldak', 'TR-68': 'Aksaray', 'TR-69': 'Bayburt', 'TR-70': 'Karaman',
    'TR-71': 'Kırıkkale', 'TR-72': 'Batman', 'TR-73': 'Şırnak', 'TR-74': 'Bartın', 'TR-75': 'Ardahan',
    'TR-76': 'Iğdır', 'TR-77': 'Yalova', 'TR-78': 'Karabük', 'TR-79': 'Kilis', 'TR-80': 'Osmaniye',
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
    'ZA': 'Güney Afrika'
}"""

pattern = re.compile(r'CITIES = \{.*?\n\}', re.DOTALL)
new_content = pattern.sub(correct_cities, content)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("CITIES updated successfully.")
