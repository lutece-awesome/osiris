from requests import post
from . import JudgeQueue

def upload_result( report ):
    '''
        Send the report to the server
    '''
    print( report.attribute )
    JudgeQueue.result.put( report.attribute )
