# class consists of
# name: station name
# buffer: customer queue
# delay_per_item: service time
# CustomerWaiting, busy: possible states of this station
from time import sleep

from Customer import Customer


class Station:
    def __init__(self, delay_per_item: int, name: str) -> None:
        self.delay_per_item = delay_per_item
        self.name = name

        self.buffer = []
        self.busy = False

    def anstellen(self, customer: Customer):
        self.buffer.append(customer)
        self.bedienen()

    def bedienen(self):
        while len(self.buffer):
            if self.busy is False:
                self.busy = True
                customer: Customer = self.buffer.pop(0)
                numItems = customer.einkaufsliste[0][2]
                sleepTime = self.delay_per_item * numItems
                sleep(sleepTime)
                Customer.served[self.name] += 1
                self.fertig()

    def fertig(self):
        self.busy = False
