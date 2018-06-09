from celery import Celery
from celeryconfig import broker
from billiard import Semaphore, Process, current_process
from settings import MAX_JUDGE_PROCESS, base_work_dir
from judger import judge_submission
from submission.models import Submission
from parser import parse
from os import path
from util.problem_locker import gloal_problem_lock
from judge_result import Judge_result


app = Celery(
    name = 'task',
    broker = broker
)

sep = Semaphore( MAX_JUDGE_PROCESS )

def JudgingProcess( submission ):
    main , _suff = current_process().name.split( ':' )
    _suff = int( _suff ) % MAX_JUDGE_PROCESS
    name = 'Process-' + str( _suff )
    try:
        submission = parse( ** submission )
        sub = Submission( ** { ** submission , ** {
            'work_dir' : path.join( base_work_dir , name ),
            'output_limit' : 64,
            'stack_limit' : 64,
            'sourcefile': 'Main' }})
        print( name , 'got submission, start juding(%s)' % ( str( sub.submission ) )  )
        judge_submission( sub )
    except Exception as e:
        from update import upload_result
        from report.models import Report
        upload_result( Report(
            result = Judge_result.JE,
            case = 1,
            complete = True,
            submission = sub.submission,
            additional_info = str( e ) ))
        print( name , 'error happen:' , str( e ) )
    finally:
        sep.release()

@app.task( name = 'Judger.task' )
def get_submission_task( submission ):
    sep.acquire()
    Process( target = JudgingProcess , args = ( submission , ) , daemon = True ).start()

@app.task( name = 'Judger.result' )
def upload_result_into_queue( report ):
    pass