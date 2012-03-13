'''
Created on 13 Mar 2012

@author: freynaud
'''

import time
import threading
from threading import Thread



class SnapshotListener(threading.Thread):
    '''
    classdocs
    ''' 
    
    
    def __init__(self, group=None, target=None, name=None, 
        args=(), kwargs=None, verbose=None,callback=None):
        threading.Thread.__init__(self, group=group, target=target, name=name, args=args, kwargs=kwargs, verbose=verbose)
        '''
        Constructor
        '''
        Thread.__init__(self, group, target, name, args, kwargs, verbose)
        self._callback = callback;
        self.last_check = self._get_current_time_in_seconds()
        self._loop_sleep_in_seconds = 1 
    
    
    def run(self):
        while not self._is_time_travel_detected() :
            time.sleep(self._loop_sleep_in_seconds)
        
        print("snapshot event")
        if (self._callback):
            self._callback()
        
        
        
    def _is_time_travel_detected(self):
        previous = self.last_check
        current = self._get_current_time_in_seconds()
        delta = previous - current
        self.last_check = current
        if (abs(delta) > ( self._loop_sleep_in_seconds +1 )):
            print("system time travelled "+str(delta)+" seconds.")
            return True
        else :
            return False
        
    def _get_current_time_in_seconds(self):
        now = time.time()
        seconds = int(round(now))
        print(time.strftime("%X",time.gmtime(now)))
        return seconds

    
if __name__ == "__main__":
    
    listener = SnapshotListener()
    listener.start()
    
    
       
