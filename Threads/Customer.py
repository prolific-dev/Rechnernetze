# class consists of
# statistics variables
# and methods as described in the problem description

import threading
import time

class Customer(threading.Thread):
    served = {}
    dropped = {}
    complete = 0
    duration = 0
    duration_cond_complete = 0
    count = 0

    def __init__(self, einkaufsliste, name, t):
        threading.Thread.__init__(self)
        self.einkaufsliste = einkaufsliste
        self.name = name
        self.t = t
        Customer.count += 1
        self.stationSkipped = False
        self.einkaufsIndex = 0

    def run(self):
        from Threads.EventSimSkeleton import my_print, my_print1, SIMU_FACTOR
        my_print(f"{round(self.t)}s: Beginn Einkauf {self.name}")

        while self.einkaufsIndex < len(self.einkaufsliste):
            einkauf = self.einkaufsliste[self.einkaufsIndex]
            timeStationArrived = einkauf[0]
            station = einkauf[1]
            maxQueue = einkauf[3]
            time.sleep(timeStationArrived / SIMU_FACTOR)
            if len(station.buffer) <= maxQueue:
                my_print1(self.name, station.name, "Ankunft")
                numItems = einkauf[2]
                servEv = threading.Event()
                station.anstellen(self, numItems, servEv)
                station.arrEv.set()
                servEv.wait()
            else:
                Customer.dropped[station.name] += 1
                self.verlassen(skipped=True)
                self.stationSkipped = True

            self.einkaufsIndex += 1

        # supermarkt verlassen
        if not self.stationSkipped:
            Customer.complete += 1


    def verlassen(self, skipped=False):
        from Threads.EventSimSkeleton import my_print1, SIMU_FACTOR
        numItems = self.einkaufsliste[self.einkaufsIndex][2]
        station = self.einkaufsliste[self.einkaufsIndex][1]
        # customer duration
        duration = 0
        if not skipped:
            duration = station.delay_per_item * numItems / SIMU_FACTOR
        if skipped:
            Customer.duration += duration
        else:
            Customer.duration += duration
            Customer.duration_cond_complete += duration

        my_print1(self.name, station.name, "Verlassen")