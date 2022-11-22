# class consists of
# statistics variables
# and methods as described in the problem description
from time import sleep

from Event import Event
from EventQueue import EventQueue


class Customer:
    served = {}
    dropped = {}
    complete = 0
    duration = 0
    duration_cond_complete = 0
    count = 0

    def __init__(self, einkaufsliste, name, t):
        self.einkaufsliste = einkaufsliste
        self.name = name
        self.t = t
        Customer.count += 1

    # beginn des einkaufs
    #- Ereignis Ankunft an der ersten Station erzeugen
    #- nächstes Ereignis Beginn des Einkaufs für den gleichen KundInnen-Typ erzeugen
    def eventBeginnEinkauf(self, args=()):
        from EventSimSkeleton import my_print
        my_print(f"{self.t}: Beginn Einkauf {self.name}")
        event = Event(EventQueue.getCurentTimeStamp(), self.eventAnkuftStation, prio=1)
        EventQueue.push(event)


    #Ankun an einer Station
    #- anhand der Warteschlangenlänge überprüfen, ob an der Station eingekauft wird
    #- wenn eingekauft wird, entweder einreihen in die Warteschlange (Systemzustand ändern)
    #  oder im Falle einer direkten Bedienung das Ereignis Verlassen der Sta on erzeugen
    #- wenn nicht eingekauft wird, direkt das Ereignis Ankunft an der nächsten Station erzeugen
    def eventAnkuftStation(self, args=()):
        from EventSimSkeleton import my_print1
        einkauf = self.einkaufsliste[0]
        tStation = einkauf[0] # dauer bis ankunft bei station
        print(f"sleep time ankunft station {tStation}")
        sleep(tStation)
        station = einkauf[1]


        my_print1(self.name, station.name, "Ankunft")

        maxQueue = einkauf[3]

        # verlassen bei max queue
        if len(station.buffer) <= maxQueue:
            station.anstellen(self)
        else:
            Customer.dropped[station.name] += 1

        event = Event(EventQueue.getCurentTimeStamp(), self.eventVerlassenStation, prio=2)
        EventQueue.push(event)


    # Verlassen einer Station
    #- Ereignis Ankun an der nächsten Station erzeugen
    #- wenn sich weitere KundInnnen in der Warteschlange be nden, erste KundIn aus der
    # Warteschlange nehmen und Ereignis Verlassen der Sta on für die nächste KundIn
    # erzeugen
    def eventVerlassenStation(self, args=()):
        from EventSimSkeleton import my_print1

        einkauf = self.einkaufsliste.pop(0)
        station = einkauf[1]

        my_print1(self.name, station.name, "Verlassen")

        einkauf = self.einkaufsliste

        if len(einkauf):
            event = Event(EventQueue.getCurentTimeStamp(), self.eventAnkuftStation, prio=3)
            EventQueue.push(event)
        else:
            Customer.complete += 1