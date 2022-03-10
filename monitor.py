from multiprocessing import Condition, Value, Lock

class Table(): 
    def __init__(self, NPHIL, manager):
        self.mutex = Lock()
        self.phil = None 
        self.NPHIL = Value('i', 0)
        #self.manager = manager
        #self.manager.list_phil = [True]*NPHIL
        self.list_phil = manager.list([False for i in range(NPHIL)])
        self.freefork = Condition(self.mutex)
        

    def free_fork(self):
        #print("a:", ((self.set_current_phil-1) % len(self.list_phil)), self.set_current_phil, len(self.list_phil))
        #print("b:", ((self.set_current_phil+1) % len(self.list_phil)), self.set_current_phil, len(self.list_phil))
        return not self.list_phil[(self.set_current_phil-1) % len(self.list_phil)] and not self.list_phil[(self.set_current_phil+1) % len(self.list_phil)]

    def set_current_phil(self, num):
        self.set_current_phil = num
    
    def wants_eat(self):
        self.mutex.acquire()
        self.freefork.wait_for(self.free_fork)
        self.list_phil[self.set_current_phil] = True 
        self.mutex.release()

    def wants_think(self): 
        self.mutex.acquire()
        self.list_phil[self.set_current_phil] = False
        self.freefork.notify_all() 
        self.mutex.release()

