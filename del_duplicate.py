with open('app.py', 'r', encoding='utf-8') as f:
    c = f.read()

# Find first
first = c.find("def apply_menus_to_all_html():")
# Find second
second = c.find("def apply_menus_to_all_html():", first + 10)

if second != -1:
    # Find end of second
    end_of_second = c.find("\n@app.route", second)
    if end_of_second == -1:
        end_of_second = len(c)
    
    # Remove second
    c = c[:second] + c[end_of_second:]
    
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(c)
    print("Deleted the second apply_menus_to_all_html")
else:
    print("Second one not found.")
