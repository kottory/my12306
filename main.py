from src.gui import Application
from src.info import Info
import os

if __name__ == "__main__":
    info = Info('data')
    app = Application(info)
    print(type(app.master))
    app.master.title('my 12306')
    if os.path.isfile('img/favicon.ico'):
        app.master.iconbitmap('img/favicon.ico')
    app.mainloop()