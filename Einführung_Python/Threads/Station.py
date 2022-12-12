# class consists of
# name: station name
# buffer: customer queue
# delay_per_item: service time
# CustomerWaiting, busy: possible states of this station
import threading
import time

from Threads.Customer import Customer

lock = threading.Lock()


class Station(threading.Thread):
    def __init__(self, delay_per_item: int, name: str) -> None:
        threading.Thread.__init__(self)

        self.delay_per_item = delay_per_item
        self.name = name
        self.buffer = []
        self.busy = False

        self.CustomerWaitingEv = threading.Event()

    def run(self):
        while True:
            self.CustomerWaitingEv.wait()  # warten bis sich jemand anstellt
            if self.buffer:
                self.bedienen()
            else:
                self.CustomerWaitingEv.clear()  # erneut auf neuen kunden warten

    def anstellen(self, customer, numItems, servEv):
        from Threads.EventSimSkeleton import my_print2
        my_print2(self.name, "neuer Kunde angestellt:", customer.name)
        lock.acquire()
        self.buffer.append((customer, numItems, servEv))
        lock.release()
        self.CustomerWaitingEv.set()  # kunde in schlange, bedienung starten

    def bedienen(self):
        from Threads.EventSimSkeleton import my_print2, SIMU_FACTOR
        self.busy = True
        lock.acquire()
        customer, numItems, servEv = self.buffer.pop(0)
        lock.release()
        my_print2(self.name, "bedient", customer.name)
        time.sleep(numItems * self.delay_per_item / SIMU_FACTOR)
        servEv.set()  # kunde wurde bedient und kann zur nächsten station
        Customer.served[self.name] += 1
        customer.verlassen()
        if self.buffer:
            self.bedienen()
        else:
            self.busy = False

    def __str__(self):
        return f'name: {self.name}' \
               f'delay per item: {self.delay_per_item}' \
               f'buffer: {self.buffer}' \
               f'busy: {self.busy}'
