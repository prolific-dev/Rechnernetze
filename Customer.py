# class consists of
# statistics variables
# and methods as described in the problem description
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
        print("beginn einkauf")
        timestampTodo = 0
        #sleep(args[0])

        event = Event(timestampTodo, self.eventAnkuftStation, prio=1)
        EventQueue.push(event)

        timestampTodo = 0
        event = Event(timestampTodo, self.eventBeginnEinkauf, prio=1)
        EventQueue.push(event)

    #Ankun an einer Station
    #- anhand der Warteschlangenlänge überprüfen, ob an der Station eingekauft wird
    #- wenn eingekauft wird, entweder einreihen in die Warteschlange (Systemzustand ändern)
    #  oder im Falle einer direkten Bedienung das Ereignis Verlassen der Sta on erzeugen
    #- wenn nicht eingekauft wird, direkt das Ereignis Ankunft an der nächsten Station erzeugen
    def eventAnkuftStation(self, args=()):
        print("ankunft station")

    # Verlassen einer Station
    #- Ereignis Ankun an der nächsten Station erzeugen
    #- wenn sich weitere KundInnnen in der Warteschlange be nden, erste KundIn aus der
    # Warteschlange nehmen und Ereignis Verlassen der Sta on für die nächste KundIn
    # erzeugen
    def eventVerlassenStation(self, args=()):
        print("verlasse station")
        #einkauf fertig? sonst naechste station anstellen

