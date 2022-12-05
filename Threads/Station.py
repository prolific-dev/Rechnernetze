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

        self.arrEv = threading.Event()

    def run(self):
        while True:
            self.arrEv.wait()
            if self.buffer:
                self.bedienen()
            else:
                self.arrEv.clear()


    def anstellen(self, customer, simutime, servEv):
        from Threads.EventSimSkeleton import my_print2
        my_print2(self.name, "neuer Kunde angestellt:", customer.name)
        lock.acquire()
        self.buffer.append((customer, simutime, servEv))
        lock.release()

    def bedienen(self):
        from Threads.EventSimSkeleton import my_print2, SIMU_FACTOR
        self.busy = True
        lock.acquire()
        customer, stationTime, servEv = self.buffer.pop(0)
        lock.release()
        my_print2(self.name, "bedient", customer.name)
        time.sleep(stationTime * self.delay_per_item / SIMU_FACTOR)
        servEv.set()
        Customer.served[self.name] += 1
        customer.verlassen()
        if not self.buffer:
            self.busy = False

    def __str__(self):
        return f'name: {self.name}' \
               f'delay per item: {self.delay_per_item}' \
               f'buffer: {self.buffer}' \
               f'busy: {self.busy}'
