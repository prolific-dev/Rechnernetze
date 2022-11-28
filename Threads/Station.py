# class consists of
# name: station name
# buffer: customer queue
# delay_per_item: service time
# CustomerWaiting, busy: possible states of this station
from threading import Thread, Event, Lock
from time import sleep

from Customer import Customer

mutex = Lock()


class Station(Thread):
    def __init__(self, delay_per_item: int, name: str) -> None:
        Thread.__init__(self)
        self.delay_per_item = delay_per_item
        self.name = name
        self.buffer = []
        self.busy = False

        #self.CustomerWaitingEv = Event()

    def anstellen(self, customer: Customer):
        mutex.acquire()
        self.buffer.append(customer)
        import EventSimSkeleton
        EventSimSkeleton.my_print2(self.name, "neuer Kunde angestellt:", customer.name)
        mutex.release()
        if not self.busy:
            self.bedienen()

    def bedienen(self):
        import EventSimSkeleton
        self.busy = True
        # print(f"{EventQueue.getCurentTimeStamp()}:{self.name} is busy")
        while len(self.buffer):
            mutex.acquire()
            customer: Customer = self.buffer.pop(0)
            mutex.release()
            numItems = customer.einkaufsliste[0][2]
            sleepTime = self.delay_per_item * numItems / EventSimSkeleton.simuFactor
            # print(f'{self.name} sleeptime {sleepTime}')
            sleep(sleepTime)
            EventSimSkeleton.my_print2(self.name, "bedient", customer.name)
            Customer.served[self.name] += 1
            customer.verlassen()
        self.fertig()

    def fertig(self):
        self.busy = False
        # print(f"{EventQueue.getCurentTimeStamp()}:{self.name} is finished")
        #self.CustomerWaitingEv.wait()

    def __str__(self):
        return f'name: {self.name}' \
               f'delay per item: {self.delay_per_item}' \
               f'buffer: {self.buffer}' \
               f'busy: {self.busy}'
