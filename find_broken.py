import glob

for f in glob.glob('**/*.html', recursive=True):
    try:
        content = open(f, encoding='utf-8', errors='ignore').read()
        if 'title="" target="_blank">' in content:
            print(f)
            break
    except:
        pass
