import glob

js_code = """
<script id="dynamic-menu-script">
document.addEventListener("DOMContentLoaded", function() {
    fetch('/api/menu')
        .then(response => response.json())
        .then(data => {
            var dropdowns = document.querySelectorAll('a.dropdown-toggle');
            dropdowns.forEach(function(el) {
                if (el.textContent.includes('Derneğimiz')) {
                    var ul = el.nextElementSibling;
                    if (ul && ul.tagName === 'UL') {
                        ul.innerHTML = '';
                        data.forEach(function(item) {
                            ul.innerHTML += '<li><a href="/dernegimiz/' + item.slug + '" target="_self">' + item.title + '</a></li>';
                        });
                        ul.innerHTML += '<li><a href="#" target="_self">Üyelerimiz</a></li>';
                    }
                }
            });
            var leftMenu = document.getElementById('left-menu');
            if (leftMenu) {
                leftMenu.innerHTML = '';
                data.forEach(function(item) {
                    leftMenu.innerHTML += '<li><a href="/dernegimiz/' + item.slug + '" target="_self">» ' + item.title + '</a></li>';
                });
                var otherItems = [
                    {title: 'Projeler', link: '#'},
                    {title: 'Gençlik Kolları', link: 'index-1.htm?mod=page&id=5'},
                    {title: 'Üyelerimiz', link: ''},
                    {title: 'Haberler', link: 'haber-listesi-1.html'},
                    {title: 'Duyurular', link: ''},
                    {title: 'Etkinlikler', link: 'etkinlikler.html'},
                    {title: 'Raporlar / Belgeler', link: ''},
                    {title: 'Fotoğraf Galerisi', link: 'resimler.html'}
                ];
                otherItems.forEach(function(item) {
                    leftMenu.innerHTML += '<li><a href="' + item.link + '" target="_self">» ' + item.title + '</a></li>';
                });
            }
        });
});
</script>
</body>
"""

for filepath in glob.glob("*.html") + glob.glob("*.htm"):
    if filepath.startswith('temp_demo') or filepath.startswith('layout'): continue
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    if 'id="dynamic-menu-script"' not in content:
        content = content.replace('</body>', js_code)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
print("Injection complete!")
