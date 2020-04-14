import os
import json


class Info:
    r"""
    Description:
        用于维护车次以及订单的信息.

    Args:
        dataDirname (str): 数据的储存地址

    Attributes:
        dataDirname (str): 数据的储存地址
        shifts (dict): 储存车次信息, 内容为 (dict)
            车次编号 (str) : 该编号车次的信息 (dict). 内容为 (dict)
                "id" : 该车次编号 (str).
                "all" : 总票数 (int).
                "station" : 站点的列表 (list), 内容为从起点站到终点站依次排列的所有站点名 (str).
                "bought" : 各站的已购票数信息的列表 (list), 内容为对应站的已购票数 (int).
        tickets (dict): 储存订单信息, 内容为 (dict)
            订单编号 (str) : 该编号订单的信息 (dict). 内容为 (dict)
            "id" : 该订单编号 (str).
            "shiftId" : 该订单对应车次 (str).
            "start" : 始发站 (str).
            "end" : 目的站 (str).
            "amount" : 已购票数 (int).

    """

    def __init__(self, dataDirname=''):
        self.shifts = {}
        self.tickets = {}
        self.dataDirname = dataDirname

    def str_to_shift_info(self, infoString):
        """
        Description:
            将要求格式的车次信息字符串转化为可被本类识别的格式. 不检查字符串格式是否正确.

        Args:
            infoString (str): 给定的信息字符串

        Returns:
            与 shifts 格式一致的车次信息 (dict)
        """
        di = {}
        infoString = infoString.strip()[:-1]
        di["id"], tmp = infoString.split(',')
        tmp = [x.strip() for x in tmp.split('|')]
        di["all"] = int(tmp[0])
        di["station"] = tmp[1:]
        di["bought"] = [0 for x in tmp[1:]]
        return di

    def load(self):
        """从 DataDirname 加载信息, 不检查信息是否合法"""
        if os.path.isfile(os.path.join(self.dataDirname, 'shift.json')):
            with open(os.path.join(self.dataDirname, 'shift.json'), 'r') as f:
                self.shifts = json.load(f)
        if os.path.isfile(os.path.join(self.dataDirname, 'ticket.json')):
            with open(os.path.join(self.dataDirname, 'ticket.json'), 'r') as f:
                self.tickets = json.load(f)

    def save(self):
        """将信息保存至 DataDirname, 覆盖原有信息"""
        if not os.path.isdir(self.dataDirname):
            os.mkdir(self.dataDirname)
        with open(os.path.join(self.dataDirname, 'shift.json'), 'w') as f:
            json.dump(self.shifts, f)
        with open(os.path.join(self.dataDirname, 'ticket.json'), 'w') as f:
            json.dump(self.tickets, f)

    def load_from_file(self, filename):
        """从 filename (str)载入信息, 格式为要求的信息字符串"""
        self.shifts = {}
        self.tickets = {}
        for line in open(filename, 'r'):
            line = line.strip()
            di = self.str_to_shift_info(line)
            self.shifts[di["id"]] = di

    def all_id(self):
        """返回所有车次的编号 (str)"""
        return sorted(list(self.shifts.keys()))

    def all_station(self):
        """返回所有站点的编号 (str)"""
        ret = []
        for shift in self.shifts.values():
            ret.extend(shift['station'])
        return sorted(list(set(ret)))

    def all_way(self, A, B):
        """返回所有自 A 可达 B 的车次信息 (list), 内容为 车次编号,已购数量,总票数 组成的三元组 (tuple)"""
        ret = []
        if A == B:
            return ret
        for shift in self.shifts.values():
            if A in shift['station']:
                i = shift['station'].index(A)
                if B in shift['station'][i:]:
                    j = shift['station'][i:].index(B)
                    b = max(shift['bought'][i:i+j])
                    ret.append((shift['id'], b, shift['all']))
        return ret

    def all_ticket_id(self):
        """返回所有订单编号的列表 (list), 内容为字典序排序后的订单编号 (str)"""
        return sorted(list(self.tickets.keys()))

    def add_shift(self, infoString):
        """从给定的信息字符串 (str) 添加车次信息"""
        shift = self.str_to_shift_info(infoString)
        self.shifts[shift['id']] = shift

    def del_shift(self, delId):
        """从给定的车次编号 (str) 删除车次信息"""
        del self.shifts[delId]

    def new_id(self):
        """新建订单编号并返回 (str)"""
        from random import randint
        ret = str(randint(1000000, 9999999))
        while ret in self.tickets.keys():
            ret = str(randint(1000000, 9999999))
        return ret

    def buy_ticket(self, bid, A, B, num):
        """
        Description:
            创建订单, 修改车次的购买信息, 并赋以唯一的订单号. 不检查该订单是否合法.
        
        Args:
            bid (str): 购买的车次编号.
            A (str): 始发站.
            B (str): 目的站.
            num (int): 购买票数
        """
        shift = self.shifts[bid]
        if A in shift['station']:
            i = shift['station'].index(A)
            if B in shift['station'][i:]:
                j = shift['station'][i:].index(B)
                for x in range(i, j):
                    shift['bought'][x] += num

        nid = self.new_id()
        self.tickets[nid] = {
            "id": nid,
            "shiftId": bid,
            "start": A,
            "end": B,
            "amount": num
        }


    def refund(self, rid):
        """删除编号号为 rid (str)的订单, 不检查删除是否合法"""
        ticket = self.tickets[rid]
        sid = ticket['shiftId']
        A = ticket['start']
        B = ticket['end']
        shift = self.shifts[sid]
        if A in shift['station']:
            i = shift['station'].index(A)
            if B in shift['station'][i:]:
                j = shift['station'][i:].index(B)
                for x in range(i, j):
                    shift['bought'][x] -= ticket['amount']
        del self.tickets[rid]
