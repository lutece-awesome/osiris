import queue
from submission.models import Submission, parse
from multiprocessing.managers import BaseManager
from multiprocessing import Process
from util.communication import task, result
from settings import MAX_JUDGE_PROCESS , base_work_dir
from os import path
from judger import judge_submission


def JudgingProcess( name ):
    while True:
        try:
            n = task.get( block = True )
            n = parse( ** n )
            sub = Submission( ** { ** n , ** {
                'work_dir' : path.join( base_work_dir , name ),
                'output_limit' : 64,
                'stack_limit' : 64,
                'sourcefile': 'main' }})
            print( name , 'got submission, start juding(%s)' % ( str( sub.submission ) )  )
            judge_submission( sub )
        except BrokenPipeError:
            print( 'Lutece Connection lost' )
            return
        except Exception as e:
            print( name , 'error happen:' , str( e ) )
    
Pool = []
for _ in range( MAX_JUDGE_PROCESS ):
    t = Process( target = JudgingProcess , args = ( 'Process-' + str( _ ) , ) , daemon = True )
    Pool.append( t )
    t.start()

for _ in Pool:
    _.join()