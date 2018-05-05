from multiprocessing.managers import BaseManager
import queue

class QueueManager(BaseManager):
    pass

QueueManager.register('get_task_queue')
QueueManager.register('get_result_queue')
print( 'Connect to Lutece %s:%s.' % ( FETCH_SUBMISSION_ADDR , FETCH_SUBMISSION_PORT ) )
m = QueueManager(address=(FETCH_SUBMISSION_ADDR, FETCH_SUBMISSION_PORT), authkey = FETCH_SUBMISSION_AUTHKEY )
m.connect()
task = m.get_task_queue()
result = m.get_result_queue()
print( 'Connect build complete' )