
from submission.models import Submission
from judger import judge_submission


def test_judge_from_file():
    judge_submission(
        submission = Submission(
            submission = 4 ,
            language = 'GNU G++17',
            code = open( 'testcase/good_cpp.cpp' , "r" ).read(),
            sourcefile = 'main-1',
            time_limit = 5000,
            memory_limit = 64,
            checker = 'wcmp',
            problem = 1,
        )
    )




if __name__ == '__main__':
    test_judge_from_file()