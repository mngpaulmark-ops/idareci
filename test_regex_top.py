import re
c=open('anasayfa.html', encoding='utf-8', errors='ignore').read()
pattern_top = r'(<nav class="collapse navbar-collapse bs-navbar-collapse" id="bs-example-navbar-collapse-1">\s*)<ul class="nav navbar-nav">.*?</ul>(\s*</nav>)'
match = re.search(pattern_top, c, flags=re.DOTALL)
print("MATCH TOP:", bool(match))
