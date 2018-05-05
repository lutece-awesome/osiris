
from submission.models import Submission
from judger import judge_submission
import threading  
import time
from compiler import compile
from settings import base_work_dir
from os import path
from util.puller import pull, pull_data
from util import puller


def test_judge_from_file():
    print( judge_submission(
        submission = Submission(
            submission = 10 ,
            language = 'GNU G++17',
            code = open( 'work/Process-0/main.cpp' , "r" ).read(),
            sourcefile = 'main',
            time_limit = 1494,
            memory_limit = 1022,
            output_limit = 64,
            stack_limit = 64,
            checker = 'wcmp',
            work_dir = path.join( base_work_dir , 'Process-0' ),
            problem = 1,
        )
    ) )


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
    # test_judge_from_file()
    print( puller.pull_data( 1 , 'test-data' ) )