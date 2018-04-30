from util.get import fetch_waiting_submission
from submission.models import Submission
from judger import judge_submission

def run_judge_thread( sourcefile ):
    s = fetch_waiting_submission()
    if s == None:
        return
    judge_submission(submission = Submission(
        submission = s['submission_id'],
        problem = s['problem'],
        code = s['code'],
        time_limit = s['time_limit'],
        memory_limit = s['memory_limit'],
        language = s['language'],
        output_limit = 64, # default 64mb
        stack_limit = 64, # default 64mb
        checker = s['checker'],
        sourcefile = sourcefile))



if __name__ == '__main__':
    run_judge_thread( 'main-1' )
