import re, glob
for f in glob.glob('**/*.html', recursive=True):
    try:
        with open(f, 'r', encoding='utf-8') as file:
            c = file.read()
        new_c = c.replace('src="/themes/', 'src="themes/')
        new_c = new_c.replace('href="/themes/', 'href="themes/')
        new_c = new_c.replace('src="/data/', 'src="data/')
        new_c = new_c.replace('href="/data/', 'href="data/')
        if new_c != c:
            with open(f, 'w', encoding='utf-8') as file:
                file.write(new_c)
    except:
        pass
print("Done")
