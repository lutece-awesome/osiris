from util.puller import pull, get_case_number, get_data_dir
from util.problem_locker import gloal_problem_lock
from update import upload_result
from report.models import Report
from compiler import compile
from runner import run

def judge_submission( submission ):
    '''
        Judge the target submission
    '''
    st , info = pull( lock = gloal_problem_lock.get( submission.problem ) , problem = submission.problem )
    if st == False:
        upload_result( Report(
            result = 'Judger Error',
            case = 1,
            submission = submission.submission,
            additional_info = 'Can not pull data',
            complete = True))
        raise RuntimeError( "Pull error: " + str( info ) )
    result , information = compile( 
        submission = submission)
    if result == 'Judger Error' or result == 'Compile Error':
        upload_result( Report(
            result = result,
            case = 1,
            submission = submission.submission,
            additional_info = information,
            complete = True))
        if result == 'Judger Error':
            raise RuntimeError( "Judger Error during compiling: " + str( information ) )
        return
    submission.case_number = get_case_number( submission.problem )
    submission.data_dir = get_data_dir( get_data_dir( submission.problem ) )
    run( sub = submission )