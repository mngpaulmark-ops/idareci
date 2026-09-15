import glob
import re

count = 0
for f in glob.glob('**/*.html', recursive=True):
    try:
        with open(f, 'r', encoding='utf-8', errors='ignore') as file:
            c = file.read()
            
        original_c = c
        
        # We want to find:
        # <div class="pull-right">
        #       /" title="" target="_blank"> (or Mebir.NET or anything broken)
        # </div>
        # And replace it with Biz Birlikte Güçlüyüz.
        
        # A safer regex: find <div class="copyright pull-left">...</div> <div class="pull-right">...</div>
        
        pattern = re.compile(r'(<div class="copyright pull-left">.*?</div>\s*<div class="pull-right">)(.*?)(</div>)', re.DOTALL | re.IGNORECASE)
        
        def replacer(match):
            return match.group(1) + '\n\t\t\t\t\t\t\t\t Biz Birlikte G\u00fc\u00e7l\u00fcy\u00fcz\n\t\t\t\t\t\t' + match.group(3)
            
        new_c = re.sub(pattern, replacer, c)
        
        # Also let's fix if there are any lingering /" title="" target="_blank"&gt; loose in the file
        new_c = new_c.replace('/" title="" target="_blank"&gt;', '')
        new_c = new_c.replace('/" title="" target="_blank">', '')
        
        if new_c != original_c:
            with open(f, 'w', encoding='utf-8') as file:
                file.write(new_c)
            count += 1
            
    except Exception as e:
        pass

print(f"Fixed footer in {count} files.")
