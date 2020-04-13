import os
import ctypes
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import tkinter.font as tkFont
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.simpledialog import askstring


def on_load(f):
    def wrapper(self):
        self.statusText.set("加载中...")
        f(self)
        self.statusText.set("加载成功!")
    return wrapper


def on_save(f):
    def wrapper(self):
        self.statusText.set("保存中...")
        f(self)
        self.statusText.set("保存成功!")
    return wrapper


def on_delete(f):
    def wrapper(self):
        self.statusText.set("删除中...")
        f(self)
        self.statusText.set("删除成功!")
    return wrapper


def hi_dpi():
    if os.name == "nt":
        ctypes.windll.shcore.SetProcessDpiAwareness(1)


class AskShiftIdWindow(Toplevel):
    def ok(self):
        self.parent.selectedId = self.opt.get()
        self.destroy()

    def createWidgets(self):
        self.text = Label(self, text='请选择车次')
        self.text.pack()

        self.optionList = self.parent.info.all_id()
        self.opt = Combobox(self, values=self.optionList)
        self.opt.current(0)
        self.opt.pack()

        self.quitButton = Button(self, text='确定', command=self.ok)
        self.quitButton.pack()

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.resizable(0, 0)
        self.createWidgets()


class AskStationWindow(Toplevel):
    def ok(self):
        self.parent.startStation = self.startOpt.get()
        self.parent.endStation = self.endOpt.get()
        self.destroy()

    def createWidgets(self):
        self.text = Label(self, text='请选择车次')
        self.text.pack()

        optionList = self.parent.info.all_station()
        self.startOpt = Combobox(self, values=optionList)
        self.startOpt.current(0)
        self.endOpt = Combobox(self, values=optionList)
        self.endOpt.current(0)

        self.startOpt.pack()
        self.endOpt.pack()

        self.quitButton = Button(self, text='确定', command=self.ok)
        self.quitButton.pack()

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.resizable(0, 0)
        self.createWidgets()


class AskOrderWindow(Toplevel):
    def ok(self):
        self.parent.boughtId = self.opt.get()
        if self.parent.boughtId and self.input.get().isdigit() and self.minval <= int(self.input.get()) <= self.restAmount[self.parent.boughtId][0]:
            self.parent.boughtAmount = int(self.input.get())
        else:
            messagebox.showwarning('错误', '输入不合法或剩余票数不足!')
            self.parent.boughtAmount = 0

        self.destroy()

    def createWidgets(self):
        def opt_selected(event):
            shift = self.opt.get()
            amount = self.restAmount[shift]
            self.showText.set('已选择%s, 总票数为%s, 剩余%s' %
                              (shift, amount[1], amount[0]))
            self.maxval = amount[0]
            self.input.config(from_=self.minval, to=self.maxval)
            self.input.set(0)

        def verify(text, prevText):
            if (text == '' or text.isdecimal() and self.minval <= int(text) <= self.maxval):
                return True
            else:
                self.input.set(prevText)
                print("Error!")
                return False
        verifyRegistered = self.register(verify)
        self.showText = StringVar()
        self.showText.set('请选择车次')
        self.shiftLabel = Label(self, textvariable=self.showText)
        self.shiftLabel.pack()

        self.minval = 0
        self.maxval = 0

        self.optionList = []
        self.restAmount = {}
        for shift, bought, total in self.sbtl:
            self.optionList.append(shift)
            self.restAmount[shift] = (total - bought, total)

        self.opt = Combobox(self, values=self.optionList)
        self.opt.pack()

        self.ticketLabel = Label(self, text='请选择张数')
        self.ticketLabel.pack()
        self.input = Spinbox(self, from_=self.minval, to=self.maxval,
                             validate='key', validatecommand=(verifyRegistered, '%P', '%s'))
        self.input.set(0)
        self.opt.bind('<<ComboboxSelected>>', opt_selected)
        self.input.pack()

        self.quitButton = Button(self, text='确定', command=self.ok)
        self.quitButton.pack()

    def __init__(self, parent=None, sbtl=None):
        super().__init__()
        self.parent = parent
        self.resizable(0, 0)
        self.sbtl = sbtl
        self.createWidgets()


class AskRefundWindow(Toplevel):
    def ok(self):
        self.parent.refundId = self.opt.get()
        self.destroy()

    def createWidgets(self):
        self.text = Label(self, text='请选择订单号')
        self.text.pack()

        self.opt = Combobox(self, values=self.parent.info.all_ticket_id())
        self.opt.current(0)
        self.opt.pack()

        self.quitButton = Button(self, text='确定', command=self.ok)
        self.quitButton.pack()

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.resizable(0, 0)
        self.createWidgets()


class Application(Frame):
    def __init__(self, info=None, master=None):
        hi_dpi()
        Frame.__init__(self, master)
        self.pack()
        self.master.resizable(0, 0)
        self.info = info
        self.createWidgets()
        self.load()
        self.statusText.set('初始化成功!')

    @on_load
    def to_info_by_station(self):
        self.startStation = self.endStation = None
        if self.info.shifts:
            popup = AskStationWindow(self)
            self.wait_window(popup)
        else:
            messagebox.showwarning('错误', '车次信息为空!')
            return

        self.displayText.set('按站点查询')
        self.infoTree.forget()
        self.infoTree = self.infoByStation

        children = self.infoTree.get_children()
        for item in children:
            self.infoTree.delete(item)

        sbtl = self.info.all_way(self.startStation, self.endStation)
        print(sbtl)
        for shift, bought, total in sbtl:
            self.infoTree.insert('', 'end', values=(
                shift, total - bought, total))

        self.scrollBar.config(command=self.infoTree.yview)
        self.infoTree.pack()

    @on_load
    def to_info_by_shift(self):
        self.selectedId = None
        if self.info.shifts:
            popup = AskShiftIdWindow(self)
            self.wait_window(popup)
        else:
            messagebox.showwarning('错误', '车次信息为空!')
            return

        self.displayText.set('按车次查询')
        self.infoTree.forget()
        self.infoTree = self.infoByShift

        children = self.infoTree.get_children()
        for item in children:
            self.infoTree.delete(item)
        if self.selectedId:
            shift = self.info.shifts[self.selectedId]
            for bought, stat in zip(shift['bought'], shift['station']):
                self.infoTree.insert(
                    '', 'end', values=(shift['id'], stat, shift['all'] - bought, shift['all']))

        self.scrollBar.config(command=self.infoTree.yview)
        self.infoTree.pack()

    @on_load
    def to_bought_info(self):
        self.displayText.set('我的订单')
        self.infoTree.forget()
        self.infoTree = self.boughtInfo

        children = self.infoTree.get_children()
        for item in children:
            self.infoTree.delete(item)

        for item in self.info.tickets.values():
            self.infoTree.insert('', 'end', values=(
                item['id'], item['shiftId'], item['start'], item['end'], item['amount']))

        self.scrollBar.config(command=self.infoTree.yview)
        self.infoTree.pack()

    @on_load
    def load_from_file(self):
        if messagebox.askokcancel("警告", "从文件加载信息将会清空目前所有的车次信息与订单信息，是否继续？"):
            file_path = askopenfilename()
            self.info.load_from_file(file_path)

    @on_save
    def save(self):
        self.info.save()

    @on_load
    def load(self):
        self.info.load()

    def add_shift(self):
        infos = askstring(
            title="输入", prompt="请输入列车信息\n形如<id>,<number>|<station1>|<station2>")
        self.info.add_shift(infos)
        self.to_bought_info()

    @on_delete
    def del_shift(self):
        self.selectedId = None
        if self.info.shifts:
            popup = AskShiftIdWindow(self)
            self.wait_window(popup)
        else:
            messagebox.showwarning('错误', '车次信息为空!')
            return
        if any(self.info.shifts[self.selectedId]['bought']):
            messagebox.showwarning('错误', '不能删除有订票的车次!')
        else:
            self.info.del_shift(self.selectedId)
            self.to_bought_info()

    def buy_ticket(self):
        self.to_info_by_station()
        self.boughtId = None
        self.boughtAmount = None
        sbtl = self.info.all_way(self.startStation, self.endStation)
        if sbtl:
            popup = AskOrderWindow(self, sbtl)
            self.wait_window(popup)
            if self.boughtId and self.boughtAmount > 0:
                self.info.buy_ticket(
                    self.boughtId, self.startStation, self.endStation, self.boughtAmount)
            self.to_bought_info()

    def refund(self):
        self.to_bought_info()
        self.refundId = None
        if self.info.tickets:
            popup = AskRefundWindow(self)
            self.wait_window(popup)
        else:
            messagebox.showwarning('错误', '无订单!')
        self.info.refund(self.refundId)
        self.to_bought_info()

    def createFonts(self):
        # 缺省字体
        self.bodyfont = tkFont.Font(size=15)
        for font in ('Noto Sans CJK SC Regular', '微软雅黑'):
            if font in tkFont.families():
                self.bodyfont = tkFont.Font(family=font, size=15)
                break

    def createMenu(self):
        self.menubar = Menu(self)
        fileMenu = Menu(self.menubar, tearoff=0)
        fileMenu.add_command(label="从文件录入", command=self.load_from_file)
        fileMenu.add_command(label="添加车次", command=self.add_shift)
        fileMenu.add_command(label="删除车次", command=self.del_shift)
        fileMenu.add_command(label="保存信息", command=self.save)

        infoMenu = Menu(self.menubar, tearoff=0)
        infoMenu.add_command(label="按班次显示", command=self.to_info_by_shift)
        infoMenu.add_command(label="按站点显示", command=self.to_info_by_station)

        findMenu = Menu(self.menubar, tearoff=0)
        findMenu.add_command(label="查看订单", command=self.to_bought_info)
        findMenu.add_command(label="购票", command=self.buy_ticket)
        findMenu.add_command(label="退票", command=self.refund)

        self.menubar.add_cascade(label='文件', menu=fileMenu)
        self.menubar.add_cascade(label='显示', menu=infoMenu)
        self.menubar.add_cascade(label='个人中心', menu=findMenu)
        self.master.config(menu=self.menubar)

    def createTreeView(self):
        self.displayText = StringVar()
        self.displayLabel = Label(
            self, textvariable=self.displayText, font=self.bodyfont)
        self.displayLabel.pack()

        self.scrollBar = Scrollbar(self)
        self.scrollBar.pack(side='right', fill='y')

        self.boughtInfo = Treeview(
            self, columns=['1', '2', '3', '4', '5'], show='headings', yscrollcommand=self.scrollBar.set)
        self.boughtInfo.heading('1', text="订单号")
        self.boughtInfo.heading('2', text="车次")
        self.boughtInfo.heading('3', text="出发站")
        self.boughtInfo.heading('4', text="到达站")
        self.boughtInfo.heading('5', text="已购票数")

        self.infoByStation = Treeview(
            self, columns=['1', '2', '3'], show='headings', yscrollcommand=self.scrollBar.set)
        self.infoByStation.heading('1', text="车次")
        self.infoByStation.heading('2', text="剩余票数")
        self.infoByStation.heading('3', text="总票数")

        self.infoByShift = Treeview(
            self, columns=['1', '2', '3', '4'], show='headings', yscrollcommand=self.scrollBar.set)
        self.infoByShift.heading('1', text="车次")
        self.infoByShift.heading('2', text="车站")
        self.infoByShift.heading('3', text="剩余票数")
        self.infoByShift.heading('4', text="总票数")

        self.infoTree = self.boughtInfo
        self.infoTree.pack()
        self.to_bought_info()

    def createStatusBar(self):
        self.statusText = StringVar()
        self.statusBar = Label(
            self, textvariable=self.statusText, relief=SUNKEN, anchor=W)
        self.statusBar.pack(side=BOTTOM, fill=X)

    def createWidgets(self):
        self.createFonts()
        self.createMenu()
        self.createStatusBar()
        self.createTreeView()


if __name__ == "__main__":
    from info import Info
    app = Application(Info('data'))
    app.mainloop()
