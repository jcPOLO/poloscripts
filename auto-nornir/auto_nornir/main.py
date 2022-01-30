from website import create_app
from core import core

web = input("web?")
if 'n' in web:
    core.main()
    exit()
else:
    app = create_app()

if __name__ == '__main__':
    app.run(debug=True)


