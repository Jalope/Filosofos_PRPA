from multiprocessing import Condition, Value, Lock

class Table(): 
    def __init__(self, NPHIL, manager):
        self.mutex = Lock()
        self.phil = None 
        self.NPHIL = Value('i', 0)
        self.list_phil = manager.list([False for i in range(NPHIL)])
        self.freefork = Condition(self.mutex)
        self.eating = Value('i',0)       

    def free_fork(self):
        return not self.list_phil[(self.set_current_phil-1) % len(self.list_phil)] and not self.list_phil[(self.set_current_phil+1) % len(self.list_phil)]

    def set_current_phil(self, num):
        self.set_current_phil = num
    
    def wants_eat(self):
        self.mutex.acquire()
        self.freefork.wait_for(self.free_fork)
        self.list_phil[self.set_current_phil] = True 
        self.mutex.release()
        self.eating += 1


    def wants_think(self): 
        self.mutex.acquire()
        self.list_phil[self.set_current_phil] = False
        self.freefork.notify_all() 
        self.mutex.release()
        self.eating -= 1 

class CheatMonitor():
    def __init__(self):
        self.mutex = Lock()
        self.phill = None 
        self.NPHILL = Value('i',0)
