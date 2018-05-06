from requests import post
from .create_queue import result

def upload_result( report ):
    '''
        Send the report to the server
    '''
    print( report.attribute )
    result.put( report.attribute )
