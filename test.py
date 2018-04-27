from fetch import fetch_waiting_submission
from judger import judge
from compiler import Compile
import time

def fetch_test():
    r = fetch_waiting_submission()
    judge(
        submission_id = r['submission_id'],
        lang = r['language'],
        code = r['code'],
        problem = r['problem']
    )
    print( r )



if __name__ == '__main__':
    s1 = time.clock()
    #print( create_tempfile( 1 , 'GNU G++17' , '#include <iostream>' ) )
    ret = Compile(
        lang = 'GNU G++17',
        code = open( 'testcase/good.cpp' , "r" ).read(),
        thread_id = 1
    )
    print( ret )
    print( 'time cost ' , time.clock() - s1 )