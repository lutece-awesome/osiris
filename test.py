from fetch.get import fetch_waiting_submission
from judger import judge
from compiler import Compile
import time
import language

def fetch_test():
    r = fetch_waiting_submission()
    print( r )

def test_compile():
    s1 = time.clock()
    ret = Compile(
        lang = 'GNU G++17',
        code = open( 'testcase/good.cpp' , "r" ).read(),
        sourcefile = 'main-1'
    )
    print( ret )
    print( 'time cost ' , time.clock() - s1 )


def test_judge():
    print( judge(
        submission_id = 1 ,
        lang = 'GNU G++17',
        code = open( 'testcase/good_cpp.cpp' , "r" ).read(),
        sourcefile = 'main-1',
        problem = 1,
        time_limit = 5000,
        memory_limit = 64,
        checker = 'wcmp'
    ) )


if __name__ == '__main__':
    test_judge()