with open('haber/1-burokratlar-birligi-adanada.html', 'r', encoding='utf-8') as f:
    c = f.read()
start = c.find('<div class="col-md-9" id="main">')
end = c.find('</div>', start + 100)
print(c[start:start+1500])
