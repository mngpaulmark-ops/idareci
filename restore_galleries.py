import re

with open('C:/tmp/anasayfa.html', 'r', encoding='windows-1254', errors='ignore') as f:
    orig = f.read()

# Extract the galleries from original
start_str = '<div class="panel panel-cyan photo-gallery">'
end_str = '</div> <!-- .panel .panel-red .video-gallery -->'

start_idx = orig.find(start_str)
end_idx = orig.find(end_str) + len(end_str)

galleries_orig = orig[start_idx:end_idx]

# Now replace it in the current anasayfa.html
with open('anasayfa.html', 'r', encoding='utf-8', errors='ignore') as f:
    curr = f.read()

# current also has this exact start_str and end_str
c_start_idx = curr.find(start_str)
c_end_idx = curr.find(end_str) + len(end_str)

if c_start_idx != -1 and c_end_idx != -1:
    new_curr = curr[:c_start_idx] + galleries_orig + curr[c_end_idx:]
    with open('anasayfa.html', 'w', encoding='utf-8') as f:
        f.write(new_curr)
    print("Successfully replaced galleries from original.")
else:
    print("Could not find start/end in current.")
