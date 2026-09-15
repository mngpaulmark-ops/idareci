import glob
import urllib.request
import os
import bs4
import concurrent.futures

base_url = "https://burokratlarbirligi.org/"
files = [f for f in glob.glob("*.html") + glob.glob("*.htm") if os.path.getsize(f) < 5000 and not f.startswith('temp_demo') and not f.startswith('layout')]

print(f"Found {len(files)} truncated files. Downloading from live site...")

def download_file(filename):
    try:
        url = base_url + filename
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, timeout=15)
        html_content = response.read()
        
        soup = bs4.BeautifulSoup(html_content, 'lxml')
        for b in soup.find_all('base'):
            b.decompose()
            
        with open(filename, 'wb') as f:
            f.write(str(soup).encode('utf-8', errors='ignore'))
        return 1
    except Exception as e:
        print(f"Failed {filename}: {e}")
        return 0

with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    count = sum(executor.map(download_file, files))
    
print(f"Successfully recovered {count} files!")
