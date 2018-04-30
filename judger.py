from util.puller import pull, get_case_number, get_data_dir
from util.update import upload_result
from report.models import Report
from compiler import compile
from runner import run

def judge_submission( submission ):
    '''
        Judge the target submission
    '''
    if pull( submission.problem ) == False:
        upload_result( Report(
            result = 'Judger Error',
            case = 1,
            submission = submission.submission,
            additional_info = 'Can not upload data',
            complete = True))
        raise RuntimeError( "Can not pull problem" )
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
        exit( 0 )
    submission.case_number = get_case_number( submission.problem )
    submission.data_dir = get_data_dir( get_data_dir( submission.problem ) )
    run( sub = submission )