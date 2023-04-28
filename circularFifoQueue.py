
class CircularFifoQueue:
    '''This class defines a circular queue. Elements are removed from the head of the queue and added to the tail of the queue in FIFO fashion.'''
    
    def __init__(self, queueCapacity=10):
        self.queueCapacity = queueCapacity
        self.currentDequeuePosition = 0
        self.currentEnqueuePosition = 0
        self.backingArray = [None] * self.queueCapacity
        self.queueSize = 0
        
    def dequeue(self):
        '''Removes the element from the head of the queue'''
        if self.queueSize==0:
            return None
        returnItem = self.backingArray[self.currentDequeuePosition]
        self.backingArray[self.currentDequeuePosition] = None
        self.currentDequeuePosition = (self.currentDequeuePosition + 1) % self.queueCapacity
        self.queueSize -= 1
        return returnItem

    def enqueue(self, item):
        '''Add an element to the tail of the queue'''
        if self.queueSize==self.queueCapacity:
            return None
        self.backingArray[self.currentEnqueuePosition] = item
        self.currentEnqueuePosition = (self.currentEnqueuePosition + 1) % self.queueCapacity
        self.queueSize += 1
        
    def printQueue(self):
        '''Print the values of all items in the queue, in the order from head to tail'''
        print(f"Queue size: {self.queueSize}")
        for i in range(self.queueSize):
            index = (self.currentDequeuePosition + i) % self.queueCapacity
            print(f"\t{self.backingArray[index]}", end="  ->")
        print()
            

# q = CircularFifoQueue(5)
# q.enqueue(1)
# q.enqueue(2)
# q.enqueue(3)
# q.enqueue(4)