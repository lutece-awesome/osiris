from fetch.get import fetch_waiting_submission
from judger import judge
from compiler import Compile
import time

def fetch_test():
    r = fetch_waiting_submission()
    judge(
        submission_id = r['submission_id'],
        lang = r['language'],
        code = r['code'],
        problem = r['problem'],
        sourcefile = 'main-1'
    )
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

if __name__ == '__main__':
    test_compile()
