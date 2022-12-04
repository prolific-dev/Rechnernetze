# class consists of
# q: event queue
# time: current time
# evCount: counter of all popped events
# methods push, pop, and start as described in the problem description
import heapq
from heapq import heapify


class EventQueue:
    q = []
    heapify(q)
    time = 0
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
            EventQueue.time = event.t
            event.work(event.args)

    @staticmethod
    def getEventList():
        return [f'prio: {item.prio}, timestamp:{item.t}' for item in EventQueue.q]
