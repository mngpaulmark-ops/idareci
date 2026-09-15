import re
with open('app.py', 'r', encoding='utf-8') as f:
    text = f.read()

# The exact block is:
# if __name__ == "__main__":
#     with app.app_context():
#         db.create_all()
#     app.run(host="0.0.0.0", port=5005, debug=True)

search_block = """if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5005, debug=True)"""

if search_block in text:
    text = text.replace(search_block, "")
    text += "\n" + search_block + "\n"
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Moved main block to the bottom')
else:
    print('Could not find exact block')
