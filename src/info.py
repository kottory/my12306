import os
import json


class Info:
    def __init__(self, dataDirname=''):
        self.shifts = {}
        self.tickets = {}
        self.dataDirname = dataDirname

    def shift_into_to_str(self):
        return "%s,%s|%s|" % (
            self.shifts["id"],
            self.shifts["all"],
            '|'.join(self.shifts["stations"])
        )

    def str_to_shift_info(self, infoString):
        di = {}
        infoString = infoString.strip()
        infoString = infoString[:-1]
        di["id"], tmp = infoString.split(',')
        tmp = tmp.split('|')
        tmp = [x.strip() for x in tmp]
        di["all"] = int(tmp[0])
        di["station"] = tmp[1:]
        di["bought"] = [0 for x in tmp[1:]]
        return di

    def load(self):
        if os.path.isfile(os.path.join(self.dataDirname, 'shift.json')):
            with open(os.path.join(self.dataDirname, 'shift.json'), 'r') as f:
                self.shifts = json.load(f)
        if os.path.isfile(os.path.join(self.dataDirname, 'ticket.json')):
            with open(os.path.join(self.dataDirname, 'ticket.json'), 'r') as f:
                self.tickets = json.load(f)

    def save(self):
        with open(os.path.join(self.dataDirname, 'shift.json'), 'w') as f:
            json.dump(self.shifts, f)
        with open(os.path.join(self.dataDirname, 'ticket.json'), 'w') as f:
            json.dump(self.tickets, f)

    def load_from_file(self, filename):
        self.shifts = {}
        self.tickets = {}
        for line in open(filename, 'r'):
            line = line.strip()
            di = self.str_to_shift_info(line)
            self.shifts[di["id"]] = di

    def all_id(self):
        return sorted(list(self.shifts.keys()))

    def all_station(self):
        ret = []
        for shift in self.shifts.values():
            ret.extend(shift['station'])
        return sorted(list(set(ret)))

    def all_way(self, A, B):
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

    def add_shift(self, infoString):
        shift = self.str_to_shift_info(infoString)
        self.shifts[shift['id']] = shift

    def del_shift(self, delId):
        del self.shifts[delId]

    def new_id(self):
        from random import randint
        ret = str(randint(1000000, 9999999))
        while ret in self.tickets.keys():
            ret = str(randint(1000000, 9999999))
        return ret

    def buy_ticket(self, bid, A, B, num):
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

    def all_ticket_id(self):
        return sorted(list(self.tickets.keys()))

    def refund(self, rid):
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


if __name__ == "__main__":
    info = Info('data')
    print(info.str_to_shift_info('G1,100|北京南|济南西|南京南|上海虹桥|'))
    # info.load()
    # print(info.shifts)
