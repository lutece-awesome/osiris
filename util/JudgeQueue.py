from multiprocessing.managers import BaseManager
import queue
from .settings import FETCH_SUBMISSION_ADDR, FETCH_SUBMISSION_PORT, FETCH_SUBMISSION_AUTHKEY
from sys import modules

class QueueManager(BaseManager):
    pass

class _JudgeQueue:

    def __init__( self ):
        QueueManager.register('get_task_queue')
        QueueManager.register('get_result_queue')
        print( 'Connect to Lutece %s:%s.' % ( FETCH_SUBMISSION_ADDR , FETCH_SUBMISSION_PORT ) )
        m = QueueManager(address=(FETCH_SUBMISSION_ADDR, FETCH_SUBMISSION_PORT), authkey = FETCH_SUBMISSION_AUTHKEY )
        m.connect()
        self.task = m.get_task_queue()
        self.result = m.get_result_queue()
        print( 'Connect build complete' )

modules[__name__] = _JudgeQueue()