# class consists of
# q: event queue
# time: current time
# evCount: counter of all popped events
# methods push, pop, and start as described in the problem description
import heapq
from datetime import datetime


class EvQueue:
    q = []
    time = datetime.now()
    evCount = 0

    def push(self, ev):
        heapq.heappush(EvQueue.q, ev)

    def pop(self):
        EvQueue.evCount += 1
        return heapq.heappop(EvQueue.q)

    def start(self):
        pass
