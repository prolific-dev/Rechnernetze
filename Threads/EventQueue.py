# class consists of
# q: event queue
# time: current time
# evCount: counter of all popped events
# methods push, pop, and start as described in the problem description
import heapq
from datetime import datetime
from heapq import heapify
from threading import Thread


class EventQueue:
    q = []
    heapify(q)
    startTime = datetime.now()
    evCount = 0

    @staticmethod
    def push(ev):
        heapq.heappush(EventQueue.q, ev)

    @staticmethod
    def pop():
        EventQueue.evCount += 1
        return heapq.heappop(EventQueue.q)


    @staticmethod
    def start():
        while EventQueue.q:
            event = EventQueue.pop()
            thread = Thread(target=event.work, args=event.args)
            thread.start()
            thread.join()

    @staticmethod
    def getCurentTimeStamp():
        timeDelta = datetime.now() - EventQueue.startTime
        return timeDelta.seconds
