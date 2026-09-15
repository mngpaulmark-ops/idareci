import re

with open('themes/burokratlar/tema/css/style.css', 'r', encoding='utf-8') as f:
    content = f.read()

responsive_css = '''
/* GENERAL RESPONSIVE FIXES */
html, body {
    overflow-x: hidden; /* Prevent horizontal scrolling */
    width: 100%;
}

img {
    max-width: 100%;
    height: auto;
}

/* Make sure container is restricted to max screen width */
.container {
    max-width: 100%;
    overflow-x: hidden;
}

/* Fix overlapping header banner elements on mobile */
@media (max-width: 767px) {
    .slideshoww {
        display: none !important; /* Hide the background flags on mobile so they don't break layout */
    }
    
    .header-banner .logo {
        margin: 10px auto !important;
        display: block;
    }
    
    /* Make tables scrollable on mobile */
    table {
        display: block;
        width: 100%;
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
    }
    
    /* Ensure sidebars stack properly */
    .left-menu, .main, .right-menu {
        padding: 0 10px !important;
    }
}
'''

if 'GENERAL RESPONSIVE FIXES' not in content:
    content += '\n' + responsive_css

with open('themes/burokratlar/tema/css/style.css', 'w', encoding='utf-8') as f:
    f.write(content)

print("Injected responsive fixes into style.css")
