# class consists of
# name: station name
# buffer: customer queue
# delay_per_item: service time
# CustomerWaiting, busy: possible states of this station
import heapq
from time import sleep

from Customer import Customer


class Station:
    def __init__(self, delay_per_item: int, name: str) -> None:
        self.delay_per_item = delay_per_item
        self.name = name

        self.buffer = []
        self.busy = False

    def anstellen(self, customer: Customer):
        heapq.heappush(self.buffer, customer)
        self.bedienen()

    def bedienen(self):
        while len(self.buffer):
            if self.busy is False:
                customer: Customer = heapq.heappop(self.buffer)
                self.busy = True
                sleep(self.delay_per_item * customer.count)
                self.fertig()

    def fertig(self):
        self.busy = False
