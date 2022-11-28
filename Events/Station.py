# class consists of
# name: station name
# buffer: customer queue
# delay_per_item: service time
# CustomerWaiting, busy: possible states of this station
from time import sleep

from Customer import Customer
from Events.EventQueue import EventQueue


class Station:
    def __init__(self, delay_per_item: int, name: str) -> None:
        self.delay_per_item = delay_per_item
        self.name = name
        self.buffer = []
        self.busy = False

    def anstellen(self, customer: Customer):
        self.buffer.append(customer)
        if not self.busy:
            self.bedienen()

    def bedienen(self):
        import EventSimSkeleton
        self.busy = True
        #print(f"{EventQueue.getCurentTimeStamp()}:{self.name} is busy")
        while len(self.buffer):
            customer: Customer = self.buffer.pop(0)
            numItems = customer.einkaufsliste[0][2]
            sleepTime = self.delay_per_item * numItems / EventSimSkeleton.simuFactor
            #print(f'{self.name} sleeptime {sleepTime}')
            sleep(sleepTime)
            Customer.served[self.name] += 1
            customer.verlassen()
        self.fertig()

    def fertig(self):
        self.busy = False
        #print(f"{EventQueue.getCurentTimeStamp()}:{self.name} is finished")

    def __str__(self):
        return f'name: {self.name}' \
               f'delay per item: {self.delay_per_item}' \
               f'buffer: {self.buffer}' \
               f'busy: {self.busy}'