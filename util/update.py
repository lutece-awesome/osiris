from requests import post
from .settings import modify_submission_url

def upload_result( report ):
    '''
        Send the report to the server
    '''
    print( report.attribute )
    try: 
        post(
            url = modify_submission_url,
            data = report.attribute)
    except Exception as e:
        raise RuntimeError( 'Upload result error: ' + str( e ) )
