from fetch.get import fetch_waiting_submission
from judger import judge
from compiler import Compile
import time
import language

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


def test_judge():
    judge(
        submission_id = 1 ,
        lang = 'GNU G++17',
        code = open( 'testcase/good.cpp' , "r" ).read(),
        sourcefile = 'main-1',
        problem = 1
    )

def test_shell_content():
    # shell_file_content = language.running_shell_arguments.format(
    #     time_limit = '1000',
    #     memory_limit = '67108864',
    #     output_limit = '67108864',
    #     stack_limit = '67108864',
    #     checker = 'wcmp',
    #     core = 'core',
    #     sourcefile = 'main-1',
    #     data_dir = '/home/xiper/Desktop/Judge_Data/1',
    #     case_number = '30'
    # )


if __name__ == '__main__':
    test_shell_content()
