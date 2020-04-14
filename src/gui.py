from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import tkinter.font as tkFont
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.simpledialog import askstring


def on_load(f):
    """显示加载信息的装饰器"""

    def wrapper(self):
        self.statusText.set("加载中...")
        ret = f(self)
        if ret:
            self.statusText.set("加载成功!")
        else:
            self.statusText.set("加载失败!")

    return wrapper


def on_save(f):
    """显示保存信息的装饰器"""

    def wrapper(self):
        self.statusText.set("保存中...")
        ret = f(self)
        if ret:
            self.statusText.set("保存成功!")
        else:
            self.statusText.set("保存失败!")

    return wrapper


def on_delete(f):
    """显示删除信息的装饰器"""

    def wrapper(self):
        self.statusText.set("删除中...")
        ret = f(self)
        if ret:
            self.statusText.set("删除成功!")
        else:
            self.statusText.set("删除失败!")

    return wrapper


def on_buy(f):
    """显示购买信息的装饰器"""

    def wrapper(self):
        self.statusText.set("购买中...")
        ret = f(self)
        if ret:
            self.statusText.set("购买成功!")
        else:
            self.statusText.set("购买失败!")

    return wrapper


def on_refund(f):
    """显示退票信息的装饰器"""

    def wrapper(self):
        self.statusText.set("退票中...")
        ret = f(self)
        if ret:
            self.statusText.set("退票成功!")
        else:
            self.statusText.set("退票失败!")

    return wrapper


def hi_dpi():
    """win32 下设置其在高 dpi 下自适应"""
    import os
    import ctypes
    if os.name == "nt":
        ctypes.windll.shcore.SetProcessDpiAwareness(1)


class AskShiftIdWindow(Toplevel):
    r"""
    Description:
        弹出窗口, 用于询问车次, 并将获取的值传递给 parent.selectedId. 会强制在 parent 中新建该属性, 如存在将覆盖其中的值.

    Args:
        parent: 上一级界面

    Attributes:
        text (Label): 显示提示文字
        optionList (list): 所有可供选择的车次(str)列表，
        opt (ComboBox): 显示车次信息的下拉菜单
        quitButton (Button): 显示确定按钮
        parent : 上一级界面
    """

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.parent.selectedId = None
        self.resizable(0, 0)
        self.createWidgets()

    def createWidgets(self):
        """创建所有物件"""
        def ok():
            """将当前下拉菜单的选项传值与上一级界面的 selectedId 属性, 并关闭当前窗口"""
            self.parent.selectedId = self.opt.get()
            self.destroy()
        # 创建提示文字
        self.text = Label(self, text='请选择车次')
        self.text.pack()
        # 创建下拉菜单
        self.optionList = self.parent.info.all_id()
        self.opt = Combobox(self, values=self.optionList)
        self.opt.current(0)
        self.opt.pack()
        # 创建确定按钮
        self.quitButton = Button(self, text='确定', command=ok)
        self.quitButton.pack()


class AskStationWindow(Toplevel):
    r"""
    Description:
        弹出窗口, 用于询问出发站与目的站, 并将获取的值传递给 parent.startStation 与 parent.endStation. 会强制在 parent 中新建该属性, 如存在将覆盖其中的值.

    Args:
        parent: 上一级界面

    Attributes:
        text (Label): 显示提示文字
        optionList (list): 所有可供选择的车次(str)列表，
        startOpt (ComboBox): 显示出发站信息的下拉菜单
        endOpt (ComboBox): 显示目的站信息的下拉菜单
        quitButton (Button): 显示确定按钮
        parent : 上一级界面
    """

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.parent.startStation = None
        self.parent.endStation = None
        self.resizable(0, 0)
        self.optionList = self.parent.info.all_station()
        self.createWidgets()

    def createWidgets(self):
        """创建所有物件"""
        def ok():
            """将当前下拉菜单的选项传值与上一级界面的 startStaion 与 endStation 属性, 并关闭当前窗口"""
            self.parent.startStation = self.startOpt.get()
            self.parent.endStation = self.endOpt.get()
            self.destroy()
        # 创建提示文字
        self.text = Label(self, text='请选择车次')
        self.text.pack()
        # 创建始发站下拉菜单
        self.startOpt = Combobox(self, values=self.optionList)
        self.startOpt.current(0)
        self.startOpt.pack()
        # 创建目的站下拉菜单
        self.endOpt = Combobox(self, values=self.optionList)
        self.endOpt.current(0)
        self.endOpt.pack()
        # 创建确定按钮
        self.quitButton = Button(self, text='确定', command=ok)
        self.quitButton.pack()


class AskOrderWindow(Toplevel):
    """
    Description:
        弹出窗口, 用于询问购票车次与购票数量, 并将值传递与 parent.boughtId 与 parent.boughtAmount. 会强制在 parent 中新建该属性, 如存在将覆盖其中的值.

    Args:
        parent: 上级界面
        sbtl (list): 车次信息的列表, 成员为 车次,已购数量,总数量 组成的三元组.

    Attributes:
        parent: 上级界面
        minval (int): 所选车次的最少购票数
        maxval (int): 所选车次的最多购票数
        shiftLabel (Label): 显示车次信息的文字
        showText (StringVar): shiftLabel 的内容
        optionList (list): 所有可供选择的车次信息(str)列表
        restAmount (dist): 车次对应的剩余票数, 内容为
            车次(str) : 剩余票数(int)
        opt (ComboBox):显示车次信息的下拉菜单
        ticketLabel (Label): 提示文字
        input (SpinBox): 输入购买的车票数量的输入框
        quitButton (Button): 确定按钮
    """

    def __init__(self, parent=None, sbtl=None):
        super().__init__()
        self.parent = parent
        self.resizable(0, 0)
        self.optionList = []
        self.restAmount = {}
        for shift, bought, total in sbtl:
            self.optionList.append(shift)
            self.restAmount[shift] = (total - bought, total)
        self.minval = 0
        self.maxval = 0
        self.createWidgets()

    def CreateShiftSelection(self):
        """创建选择车次的控件"""
        def opt_selected(event):
            """当所选车次信息改变时, 改变购买票数的输入上下限"""
            shift = self.opt.get()
            amount = self.restAmount[shift]
            self.showText.set('已选择%s, 总票数为%s, 剩余%s' %
                              (shift, amount[1], amount[0]))
            self.maxval = amount[0]
            self.input.config(from_=self.minval, to=self.maxval)
            self.input.set(0)
        # 创建提示信息
        self.showText = StringVar()
        self.showText.set('请选择车次')
        self.shiftLabel = Label(self, textvariable=self.showText)
        self.shiftLabel.pack()
        # 创建下拉菜单
        self.opt = Combobox(self, values=self.optionList)
        self.opt.pack()
        self.opt.bind('<<ComboboxSelected>>', opt_selected)

    def CreateTicketSelection(self):
        """创建选择购买票数的控件"""
        @self.register
        def verify(text, prevText):
            """验证目前输入是否合法, 若不合法则保持之前的输入"""
            if (text == '' or text.isdecimal() and self.minval <= int(text) <= self.maxval):
                return True
            else:
                self.input.set(prevText)
                return False
        # 创建提示信息
        self.ticketLabel = Label(self, text='请选择张数')
        self.ticketLabel.pack()
        # 创建输入框
        self.input = Spinbox(self, from_=self.minval, to=self.maxval,
                             validate='key', validatecommand=(verify, '%P', '%s'))
        self.input.set(0)
        self.input.pack()

    def createWidgets(self):
        """创建所有物件"""
        def ok():
            """将当前下拉菜单与输入框的选项传值与上一级界面的 boughtId 与 boughtAmount 属性, 并关闭当前窗口"""
            self.parent.boughtId = self.opt.get()
            if self.parent.boughtId:
                if self.input.get() == '':
                    self.parent.boughtAmount = 0
                else:
                    self.parent.boughtAmount = int(self.input.get())
                self.destroy()
            else:
                messagebox.showwarning('错误', '请选择车次!')

        self.CreateShiftSelection()
        self.CreateTicketSelection()
        # 创建确定按钮
        self.quitButton = Button(self, text='确定', command=ok)
        self.quitButton.pack()


class AskRefundWindow(Toplevel):
    """
    Description:
        弹出窗口, 用于询问退票的 ID , 并将值传递与 parent.refundId. 会强制在 parent 中新建该属性, 如存在将覆盖其中的值.

    Args:
        parent: 上级界面.

    Attribute:
        parent: 上级界面.
        text (Label): 提示文字.
        opt (ComboBox): 显示订单 ID 的下拉菜单.
        quitButton (Button): 确定按钮
    """

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.parent.refundId = None
        self.resizable(0, 0)
        self.createWidgets()

    def createWidgets(self):
        """创建所有物件"""
        def ok():
            """将当前下拉菜单的选项传值与上一级界面的 refundId 属性, 并关闭当前窗口"""
            self.parent.refundId = self.opt.get()
            self.destroy()
        # 创建提示信息
        self.text = Label(self, text='请选择订单号')
        self.text.pack()
        # 创建下拉菜单
        self.opt = Combobox(self, values=self.parent.info.all_ticket_id())
        self.opt.current(0)
        self.opt.pack()
        # 创建确定按钮
        self.quitButton = Button(self, text='确定', command=ok)
        self.quitButton.pack()


class Application(Frame):
    """
    Description:
        图形界面的核心, 本项目界面的入口. 可以通过 Application(info.Info).mainloop 创建并运行界面

    Args:
        info (Info): 用于维护信息的数据结构.

    Attributes:
        -------------- 信息类 ------------
        info (Info): 用于维护所有信息
        ------------- 返回值类 -----------
        selectedId 用于接收弹窗的返回值, 详见 AskShiftIdWindow
        startStation 用于接收弹窗的返回值, 详见 AskStationWindow
        endStation 用于接收弹窗的返回值, 详见 AskStaionWindow
        boughtId 用于接收弹窗的返回值, 详见 AskOrderWindow
        boughtAmount 用于接收弹窗的返回值, 详见 AskOrderWindow
        refundId 用于接收弹窗的返回值, 详见 AskRefundWindow
        ----------- 控件类 ---------------
        displayFont (Font): 当前显示内容的标题的字体
        menubar (Menu): 显示菜单栏
        displayText (StringVar): 当前显示内容的标题的内容
        displayLabel (Label): 显示当前显示内容的标题信息
        scrollBar (ScrollBar): 显示内容的滚动条
        boughtInfo (TreeView): 显示订单的表格界面
        infoByStation (TreeView): 显示以站点信息查询的表格界面
        infoByShift (TreeView): 显示以车次信息查询的表格界面
        infoTree (TreeView): 当前显示表格界面
        statusText (StringVar): 状态栏内容
        statusBar (Label): 显示状态栏
    """

    def __init__(self, info=None):
        hi_dpi()
        Frame.__init__(self)
        self.pack()
        self.master.resizable(0, 0)
        self.info = info
        self.createWidgets()
        self.selectedId = None
        self.startStation = None
        self.endStation = None
        self.boughtId = None
        self.boughtAmount = None
        self.refundId = None
        self.load()
        self.to_bought_info()

    @on_load
    def to_info_by_station(self):
        """询问始终站并转到以站次查询的界面, 若成功则返回 True"""
        if self.info.shifts:
            popup = AskStationWindow(self)
            self.wait_window(popup)
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
            return True
        else:
            messagebox.showwarning('错误', '车次信息为空!')
            return False

    @on_load
    def to_info_by_shift(self):
        """询问车次并转到以车次查询的界面, 若成功则返回 True"""
        if self.info.shifts:
            popup = AskShiftIdWindow(self)
            self.wait_window(popup)
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
            return True
        else:
            messagebox.showwarning('错误', '车次信息为空!')
            return False

    @on_load
    def to_bought_info(self):
        """转到订单界面, 始终返回 True"""
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
        return True

    @on_load
    def load_from_file(self):
        """从文件加载信息字符串, 若成功则返回 True"""
        if messagebox.askokcancel("警告", "从文件加载信息将会清空目前所有的车次信息与订单信息，是否继续？"):
            file_path = askopenfilename()
            self.info.load_from_file(file_path)
            return True
        else:
            return False

    @on_save
    def save(self):
        """保存信息"""
        self.info.save()
        return True

    @on_load
    def load(self):
        """加载信息"""
        self.info.load()
        return True

    @on_load
    def add_shift(self):
        """弹窗询问添加信息字符串"""
        infos = askstring(
            title="输入", prompt="请输入列车信息\n形如<id>,<number>|<station1>|<station2>")
        if infos:
            self.info.add_shift(infos)
            self.to_bought_info()
            return True
        else:
            return False

    @on_delete
    def del_shift(self):
        """弹窗询问删除车次, 成功后转到订单界面, 并返回 True"""
        if self.info.shifts:
            popup = AskShiftIdWindow(self)
            self.wait_window(popup)
            if any(self.info.shifts[self.selectedId]['bought']):
                messagebox.showwarning('错误', '不能删除有订票的车次!')
                return False
            else:
                self.info.del_shift(self.selectedId)
                self.to_bought_info()
                return True
        else:
            messagebox.showwarning('错误', '车次信息为空!')
            return False

    @on_buy
    def buy_ticket(self):
        """弹窗询问购买车票, 成功后转到订单界面, 并返回 True"""
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
                return True

        self.to_bought_info()
        return False

    @on_refund
    def refund(self):
        """弹窗询问退票, 并转到订单界面, 并返回 True"""
        self.to_bought_info()
        if self.info.tickets:
            popup = AskRefundWindow(self)
            self.wait_window(popup)
            if self.refundId:
                self.info.refund(self.refundId)
                self.to_bought_info()
                return True
            else:
                return False
        else:
            messagebox.showwarning('错误', '无订单!')
            self.to_bought_info()
            return False

    def createFonts(self):
        """创建字体"""
        self.displayFont = tkFont.Font(size=15)
        for font in ('Noto Sans CJK SC Regular', '微软雅黑'):
            if font in tkFont.families():
                self.displayFont = tkFont.Font(family=font, size=15)
                break

    def createMenu(self):
        """创建菜单栏"""
        self.menubar = Menu(self)
        fileMenu = Menu(self.menubar, tearoff=0)
        fileMenu.add_command(label="从文件录入", command=self.load_from_file)
        fileMenu.add_command(label="添加车次", command=self.add_shift)
        fileMenu.add_command(label="删除车次", command=self.del_shift)
        fileMenu.add_command(label="保存信息", command=self.save)
        self.menubar.add_cascade(label='文件', menu=fileMenu)

        infoMenu = Menu(self.menubar, tearoff=0)
        infoMenu.add_command(label="按班次显示", command=self.to_info_by_shift)
        infoMenu.add_command(label="按站点显示", command=self.to_info_by_station)
        self.menubar.add_cascade(label='显示', menu=infoMenu)

        findMenu = Menu(self.menubar, tearoff=0)
        findMenu.add_command(label="查看订单", command=self.to_bought_info)
        findMenu.add_command(label="购票", command=self.buy_ticket)
        findMenu.add_command(label="退票", command=self.refund)
        self.menubar.add_cascade(label='个人中心', menu=findMenu)

        self.master.config(menu=self.menubar)

    def createTreeView(self):
        """创建表格"""
        self.displayText = StringVar()
        self.displayLabel = Label(
            self, textvariable=self.displayText, font=self.displayFont)
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

    def createStatusBar(self):
        """创建状态栏"""
        self.statusText = StringVar()
        self.statusBar = Label(
            self, textvariable=self.statusText, relief=SUNKEN, anchor=W)
        self.statusBar.pack(side=BOTTOM, fill=X)

    def createWidgets(self):
        """创建所有组件"""
        self.createFonts()
        self.createMenu()
        self.createStatusBar()
        self.createTreeView()


if __name__ == "__main__":
    from info import Info
    app = Application(Info('data'))
    app.mainloop()
