import app

with open('app.py', 'a', encoding='utf-8') as f:
    f.write('\n\nif __name__ == "__main__":\n    with app.app_context():\n        db.create_all()\n    app.run(host="0.0.0.0", port=5005, debug=False)\n')

print("Added app.run back to the bottom of app.py")
