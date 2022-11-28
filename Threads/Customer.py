# class consists of
# statistics variables
# and methods as described in the problem description
from datetime import timedelta, datetime
from threading import Thread
from time import sleep

from Event import Event
from EventQueue import EventQueue


class Customer(Thread):
    served = {}
    dropped = {}
    complete = 0
    duration = 0
    duration_cond_complete = 0
    count = 0

    def __init__(self, einkaufsliste, name, t):
        Thread.__init__(self)
        self.einkaufsliste = einkaufsliste
        self.name = name
        self.t = datetime.now() - EventQueue.startTime + timedelta(seconds=t)
        Customer.count += 1
        self.stationSkipped = False

    # beginn des einkaufs
    # - Ereignis Ankunft an der ersten Station erzeugen
    # - nächstes Ereignis Beginn des Einkaufs für den gleichen KundInnen-Typ erzeugen
    def eventBeginnEinkauf(self, *args):
        from EventSimSkeleton import my_print
        my_print(f"{self.t.seconds}s: Beginn Einkauf {self.name}")
        event = Event(EventQueue.getCurentTimeStamp(), self.eventAnkuftStation, self.einkaufsliste[0], prio=2)
        EventQueue.push(event)

    # Ankun an einer Station
    # - anhand der Warteschlangenlänge überprüfen, ob an der Station eingekauft wird
    # - wenn eingekauft wird, entweder einreihen in die Warteschlange (Systemzustand ändern)
    #  oder im Falle einer direkten Bedienung das Ereignis Verlassen der Sta on erzeugen
    # - wenn nicht eingekauft wird, direkt das Ereignis Ankunft an der nächsten Station erzeugen
    def eventAnkuftStation(self, *args):
        from EventSimSkeleton import my_print1, simuFactor
        einkauf = args
        tStation = einkauf[0] / simuFactor  # dauer bis ankunft bei station
        sleep(tStation)
        station = einkauf[1]

        my_print1(self.name, station.name, "Ankunft")

        maxQueue = einkauf[3]

        # verlassen bei max queue
        if len(station.buffer) <= maxQueue:
            station.anstellen(self)
        else:
            Customer.dropped[station.name] += 1
            self.verlassen(skipped=True)
            self.stationSkipped = True

    def verlassen(self, skipped=False):
        event = Event(EventQueue.getCurentTimeStamp(), self.eventVerlassenStation, self.einkaufsliste[0], prio=1)
        EventQueue.push(event)

        # customer duration
        duration = EventQueue.getCurentTimeStamp() - self.t.seconds
        if skipped:
            Customer.duration += duration
        else:
            Customer.duration += duration
            Customer.duration_cond_complete += duration

    # Verlassen einer Station
    # - Ereignis Ankun an der nächsten Station erzeugen
    # - wenn sich weitere KundInnnen in der Warteschlange be nden, erste KundIn aus der
    # Warteschlange nehmen und Ereignis Verlassen der Sta on für die nächste KundIn
    # erzeugen
    def eventVerlassenStation(self, *args):
        from EventSimSkeleton import my_print1

        einkauf = args
        station = einkauf[1]

        my_print1(self.name, station.name, "Verlassen")

        self.einkaufsliste.pop(0)
        if len(self.einkaufsliste):
            # station verlassen
            event = Event(EventQueue.getCurentTimeStamp(), self.eventAnkuftStation, self.einkaufsliste[0], prio=3)
            EventQueue.push(event)
        else:
            # supermarkt verlassen
            if not self.stationSkipped:
                Customer.complete += 1
