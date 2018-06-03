from util.puller import pull, get_case_number, get_data_dir
from util.problem_locker import gloal_problem_lock
from update import upload_result
from report.models import Report
from compiler import compile
from runner import run
from create_tempfile import create_tempfile
from judge_result import Judge_result


def judge_submission( submission ):
    '''
        Judge the target submission
    '''
    if submission.language is None:
        upload_result( Report(
            result = Judge_result.JE,
            case = 1,
            complete = True,            
            submission = submission.submission,
            additional_info = 'Unknown language' ))
        raise RuntimeError( 'Unknown Language' )
    else:
        upload_result( Report(
            result = Judge_result.PR,
            submission = submission.submission ))
    st , info = pull( lock = gloal_problem_lock.get( submission.problem ) , problem = submission.problem )
    if not st:
        upload_result( Report(
            result = Judge_result.JE,
            case = 1,
            complete = True,            
            submission = submission.submission,
            additional_info = 'Can not pull data' ))
        raise RuntimeError( "Pull error: " + str( info ) )
    st , info = create_tempfile(
        sourcefile = submission.sourcefile,
        work_dir = submission.work_dir,
        lang = submission.language,
        code = submission.code
    )
    if st != 'Success':
        upload_result( Report(
                result = result,
                case = 1,
                complete = True,                
                submission = submission.submission,
                additional_info = info))
        raise RuntimeError( "Judger Error during creating tempfile: " + str( info ) )
    if submission.language.value.compile is True:
        result , information = compile( 
            submission = submission)
        if result is Judge_result.JE or result is Judge_result.CE:
            upload_result( Report(
                result = result,
                case = 1,
                complete = True,
                submission = submission.submission,
                additional_info = information))
            if result is Judge_result.JE:
                raise RuntimeError( "Judger Error during compiling: " + str( information ) )
            return
    submission.case_number = get_case_number( submission.problem )
    submission.data_dir = get_data_dir( get_data_dir( submission.problem ) )
    run( sub = submission )