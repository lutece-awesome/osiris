from multiprocessing import Lock
from random import random

class Problem_lock:
    '''
        For problem pull request, multi-process lock is needed
    '''

    def _create( self , problem ):
        setattr( self , str( problem ) , Lock() )

    def get( self , problem ):
        problem = str( problem )
        if hasattr( self , problem ) == False:
            self._create( problem )
        return getattr( self , problem )

gloal_problem_lock = Problem_lock()