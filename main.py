from src.gui import Application
from src.info import Info

if __name__ == "__main__":
    info = Info('data')
    app = Application(info)
    print(type(app.master))
    app.master.title('my 12306')
    app.mainloop()