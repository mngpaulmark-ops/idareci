import glob
import re

def update_links(fb, tw):
    # Include templates folder to ensure templates also get updated
    files = glob.glob('*.html') + glob.glob('haber/*.html') + glob.glob('kose-yazilari*.html') + glob.glob('templates/*.html')
    
    # Use a more robust regex that catches any encoding variations for "Sayfamız"
    fb_pat = re.compile(r'<a href="[^"]*"\s+title="Facebook\s+Sayfam[^"]*"', re.IGNORECASE)
    tw_pat = re.compile(r'<a href="[^"]*"\s+title="Twitter\s+Sayfam[^"]*"', re.IGNORECASE)
    
    # Also in case class="facebook" is used without title
    fb_class_pat = re.compile(r'<a href="[^"]*"\s+class="facebook"')
    tw_class_pat = re.compile(r'<a href="[^"]*"\s+class="twitter"')

    for file in files:
        try:
            with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Sub with original title to avoid breaking HTML
            new_content = fb_pat.sub(f'<a href="{fb}" title="Facebook Sayfamız"', content)
            new_content = tw_pat.sub(f'<a href="{tw}" title="Twitter Sayfamız"', new_content)
            
            # If they don't have title but have class
            new_content = fb_class_pat.sub(f'<a href="{fb}" class="facebook"', new_content)
            new_content = tw_class_pat.sub(f'<a href="{tw}" class="twitter"', new_content)

            if new_content != content:
                with open(file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
        except Exception as e:
            print(f"Error in {file}: {e}")

if __name__ == '__main__':
    update_links('#', '#')
