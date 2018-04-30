
from submission.models import Submission
from judger import judge_submission
import threading  
from osiris import run_judge_thread
import time
from compiler import compile

def test_judge_from_file():
    judge_submission(
        submission = Submission(
            submission = 4 ,
            language = 'GNU G++17',
            code = open( 'testcase/good.cpp' , "r" ).read(),
            sourcefile = 'main-1',
            time_limit = 5000,
            memory_limit = 64,
            output_limit = 64,
            stack_limit = 64,
            checker = 'wcmp',
            problem = 1,
        )
    )

def multi_thread_test():
    s = []
    for i in range( 0 , 4 ):
        name = 'main-1' + str(i)
        s.append( threading.Thread(target=run_judge_thread , args = ( name, ) ) )
    for _ in s:
        _.daemon = True
        _.start()
        time.sleep( 0.2 )
    for _ in s:
        _.join()

def test_compile():
    print( compile(
        submission = Submission(
            submission = 4 ,
            language = 'GNU G++17',
            code = open( 'testcase/compile_bomb.cpp' , "r" ).read(),
            sourcefile = 'main-144',
            time_limit = 5000,
            memory_limit = 64,
            output_limit = 64,
            stack_limit = 64,
            checker = 'wcmp',
            problem = 1,
        )) )


if __name__ == '__main__':
    multi_thread_test()