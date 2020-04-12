import json
import os

class Shift:
    def __init__(self, id=0, totalTickets=None, stations=None, boughtTicketsPerStation=None):
        self.id = id
        self.totalTickets = totalTickets
        self.stations = stations
        self.boughtTicketsPerStation = boughtTicketsPerStation

    def decode_from_str(self, infoString=''):
        self.id, tmp = infoString.split(',')
        tmp = tmp.split('|')
        self.totalTickets = int(tmp[0])
        self.stations = tmp[1:]
        self.boughtTicketsPerStation = [0] * len(tmp[:1])

    def __str__(self):
        return "%s,%s|%s" % (self.id, self.totalTickets, '|'.join(self.boughtTicketsPerStation))

    def to_json(self):
        return {
            "id": self.id,
            "totalTickets": self.totalTickets,
            "stations": self.stations,
            "boughtTicketsPerStation": self.boughtTicketsPerStation
        }

    @classmethod
    def decode_from_json(cls, di):
        return Shift(di["id"], di["totalTickets"], di["stations"], di["boughtTicketsPerStation"])


class Ticket:
    def __init__(self, id='', start='', end='', amount=0):
        self.id = id
        self.start = start
        self.end = end
        self.amount = amount

    def to_json(self):
        return {
            "id": self.id,
            "start": self.start,
            "end": self.end,
            "amount": self.amount
        }

    @classmethod
    def decode_from_json(cls, di):
        return Ticket(di["id"], di["start"], di["end"], di["amount"])


class Info:
    def __init__(self, dataDirname=''):
        self.shifts = {}
        self.tickets = {}
        self.dataDirname = dataDirname

    def load(self):
        with open(os.path.join(self.dataDirname, 'shift.json', 'w')) as f:
            d = json.load(f)
            self.shifts = {}
            for shift in d.items():
                self.shifts[shift["id"]] = Shift.decode_from_json(shift)
            


if __name__ == "__main__":
    print(os.listdir())