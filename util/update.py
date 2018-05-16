from requests import post

def upload_result( report ):
    '''
        Send the report to the server
    '''
    print( report.attribute )
