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
        import EventSimSkeleton
        EventSimSkeleton.my_print2(self.name, "neuer Kunde angestellt:", customer.name)
        if not self.busy:
            self.bedienen()

    def bedienen(self):
        self.busy = True
        while len(self.buffer):
            customer: Customer = self.buffer.pop(0)
            numItems = customer.einkaufsliste[0][2]
            import EventSimSkeleton
            sleepTime = self.delay_per_item * numItems / EventSimSkeleton.simuFactor
            sleep(sleepTime / 1000)
            EventSimSkeleton.my_print2(self.name, "bedient", customer.name)
            Customer.served[self.name] += 1
            
        self.fertig()

    def fertig(self):
        self.busy = False
