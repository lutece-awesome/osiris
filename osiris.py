from celery import Celery
from submission.models import Submission
from settings import MAX_JUDGE_PROCESS
from billiard import Semaphore, Process , Lock
from settings import MAX_JUDGE_PROCESS
from judger import judge_submission


empty = Semaphore( MAX_JUDGE_PROCESS )
app = Celery( 'todo_que' , broker = 'amqp://guest@localhost//' )

def start_judge( submission , language , problem , code , tiemlimit , memorylimit , checker , sourcefile ):
    print( 'Start judging:' , submission )
    try:
        judge_submission( submission = Submission(
            submission = submission,
            language = language,
            code = code,
            time_limit = tiemlimit,
            memory_limit = memorylimit,
            output_limit = 64,
            stack_limit = 64,
            checker = checker,
            problem = problem,
            sourcefile = sourcefile))
    finally:
        empty.release()
        print( 'Judging submission:' , submission , 'completed' )


@app.task
def todo_que( submission , language , problem , code , timelimit , memorylimit , checker ):
    empty.acquire()
    t = Process( target = start_judge , args = ( submission , language , problem , code , timelimit , memorylimit , checker ) )
    t.start()