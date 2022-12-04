from copy import deepcopy

from Customer import Customer
from Event import Event
from EventQueue import EventQueue
from Station import Station

f = open("./supermarkt.txt", "w")
fc = open("./supermarkt_customer.txt", "w")
fs = open("./supermarkt_station.txt", "w")

# print on console and into supermarket log
def my_print(msg):
    print(msg)
    f.write(msg + '\n')


# print on console and into customer log
def my_print1(customerName, stationName, msg):
    text = f'{EventQueue.time}s: {customerName} {msg} at {stationName}\n'
    print(text)
    fc.write(text)


# print on console and into station log
def my_print2(stationName, msg, customerName):
    text = f'{EventQueue.time}s: {stationName} {msg} {customerName}\n'
    print(text)
    fs.write(text)


def startCustomers(einkaufsliste, name, sT, dT, mT):
    i = 1
    t = sT
    while t < mT:
        kunde = Customer(einkaufsliste, name + str(i), t)
        ev = Event(t, kunde.eventBeginnEinkauf, prio=2)
        evQ.push(ev)
        i += 1
        t += dT


if __name__ == '__main__':
    evQ = EventQueue()
    baecker = Station(10, 'Bäcker')
    metzger = Station(30, 'Metzger')
    kaese = Station(60, 'Käse')
    kasse = Station(5, 'Kasse')
    Customer.served['Bäcker'] = 0
    Customer.served['Metzger'] = 0
    Customer.served['Käse'] = 0
    Customer.served['Kasse'] = 0
    Customer.dropped['Bäcker'] = 0
    Customer.dropped['Metzger'] = 0
    Customer.dropped['Käse'] = 0
    Customer.dropped['Kasse'] = 0
    # stations bearbeitungszeit, stationsname, Anzahl zu kaufenden Produkte, MaxQueue Wartezeit
    einkaufsliste1 = [(10, baecker, 10, 10), (30, metzger, 5, 10), (45, kaese, 3, 5), (60, kasse, 30, 20)]
    einkaufsliste2 = [(30, metzger, 2, 5), (30, kasse, 3, 20), (20, baecker, 3, 20)]
    startCustomers(einkaufsliste1, 'T1/K', 0, 200, 30 * 60 + 1)
    startCustomers(einkaufsliste2, 'T2/K', 1, 60, 30 * 60 + 1)
    evQ.start()

    my_print(f'Simulationsende: {EventQueue.time}')  # letzter einkäufer fertig
    my_print(f'Anzahl Kunden: {Customer.count}')
    my_print(f'Anzahl vollständige Einkäufe {Customer.complete}')
    x = Customer.duration / Customer.count
    my_print(f'Mittlere Einkaufsdauer {x:.2f}s')
    x = 0 if Customer.complete == 0 else Customer.duration_cond_complete / Customer.complete
    my_print(f'Mittlere Einkaufsdauer (vollständig): {x:.2f}s')

    for station in ('Bäcker', 'Metzger', 'Käse', 'Kasse'):
        x = 0 if Customer.dropped[station] == 0 else Customer.dropped[station] / (Customer.served[station] + Customer.dropped[station]) * 100
        my_print(f'Drop percentage at {station}: {x:.2f}')

    f.close()
    fc.close()
    fs.close()
