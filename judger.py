from util.puller import pull, get_data_dir, get_test_case
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
        raise RuntimeError( 'Unknown Language' )
    else:
        upload_result( Report(
            result = Judge_result.PR,
            submission = submission.submission ))
    st , info = pull( lock = gloal_problem_lock.get( submission.problem ) , problem = submission.problem )
    if not st:
        raise RuntimeError( "Pull error: " + str( info ) )
    st , info = create_tempfile(
        sourcefile = submission.sourcefile,
        work_dir = submission.work_dir,
        lang = submission.language,
        code = submission.code)
    if st != 'Success':
        raise RuntimeError( "Judger Error during creating tempfile: " + str( info ) )
    if submission.language.value.compile is True:
        result , information = compile( 
            submission = submission)
        if result is Judge_result.CE:
            upload_result( Report(
                result = result,
                complete = True,
                submission = submission.submission,
                compileerror_msg = information))
            return
        elif result is Judge_result.JE:
            raise RuntimeError( "Judger Error during compiling: " + str( information ) )
    submission.case = get_test_case( submission.problem )
    if len( submission.case ) == 0:
        raise RuntimeError( "Judger Error, because there is no test-data" )
    submission.data_dir = get_data_dir( get_data_dir( submission.problem ) )
    run( sub = submission )