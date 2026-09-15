import re

with open('anasayfa.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Replace hardcoded height 332px with 100% and use flexbox, OR use JS.
# Let's use JS to exactly match the height of the first panel-body.

js_sync = """
<script>
document.addEventListener("DOMContentLoaded", function() {
    setTimeout(function() {
        var leftPanel = document.querySelector('.news .col-md-6:first-child .panel.panel-primary');
        var trtWidget = document.getElementById('trt-widget');
        var trtPanel = document.querySelector('.news .col-md-6:nth-child(2) .panel.panel-primary');
        
        if (leftPanel && trtWidget && trtPanel) {
            // Match the height of the entire panel
            trtPanel.style.height = leftPanel.offsetHeight + 'px';
            
            // Adjust the inner widget height based on the header height
            var headerHeight = trtPanel.querySelector('.panel-heading').offsetHeight;
            // padding is usually 15px top + 15px bottom for panel-body
            trtWidget.style.height = (leftPanel.offsetHeight - headerHeight - 35) + 'px';
        }
    }, 500); // Wait for images to load
});
</script>
"""

if 'trtPanel.style.height = leftPanel.offsetHeight' not in content:
    content = content.replace('<!-- .panel .panel-primary', js_sync + '\n  <!-- .panel .panel-primary')
    
    with open('anasayfa.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Height sync script injected successfully.")
else:
    print("Height sync script already exists.")
