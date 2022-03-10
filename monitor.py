from multiprocessing import Condition, Value, Lock

class Table(): 
    def __init__(self, NPHIL, manager):
        self.mutex = Lock()
        self.phil = None 
        self.NPHIL = Value('i', 0)
        #self.manager.list_phil = [True]*NPHIL
        self.list_phil = manager.list([True]*NPHIL)
        self.freefork = Condition(self.mutex)
        self.wants_eat = Condition(self.mutex)
        self.wants_think = Condition(self.mutex)

    def free_fork(self, num):
        return not self.manager.list_phil[num-1] and not self.manager.list_phil[num+1]

    def set_current_phil(self, num):
        self.set_current_phil = num
    
    def wants_eat(self, num):
        self.mutex.acquire()
        self.freefork.wait_for(self.free_fork)
        self.manager.list_phil[num] = True 
        self.mutex.release()

    def wants_think(self,num): 
        self.mutex.acquire()
        self.manager.list[num] = False
        self.freefor.notify_all() 
        self.mutex.release()
