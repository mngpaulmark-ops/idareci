import glob
import urllib.request
import os
import bs4

base_url = "https://burokratlarbirligi.org/"
files = glob.glob("*.html") + glob.glob("*.htm")

count = 0
for filename in files:
    # Check if file is essentially empty (less than 100 bytes, likely just '[]')
    if os.path.getsize(filename) < 100:
        print(f"Downloading {filename} from live site...")
        try:
            url = base_url + filename
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            response = urllib.request.urlopen(req, timeout=10)
            html_content = response.read()
            
            # Remove base tag if present
            soup = bs4.BeautifulSoup(html_content, 'lxml')
            for b in soup.find_all('base'):
                b.decompose()
                
            with open(filename, 'wb') as f:
                f.write(str(soup).encode('utf-8'))
            count += 1
        except Exception as e:
            print(f"Failed to download {filename}: {e}")

print(f"Successfully recovered {count} files from the live site!")
