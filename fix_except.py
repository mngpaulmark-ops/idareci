import re
with open('app.py', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace('''        except:
            pass''', '''        except Exception as e:
            import traceback
            traceback.print_exc()''')

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(c)

print("Updated app.py exception blocks")
