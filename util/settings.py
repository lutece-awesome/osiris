from os import path

# lutece settings
FETCH_DATA_ADDR = '127.0.0.1'
FETCH_DATA_AUTHKEY = b'772002' # in producing envir, this should be sercet
FETCH_DATA_URL =  'http://' + FETCH_DATA_ADDR + ':8000' + '/data_server/fetch/'

# md5_validator is to check whether the local file equals the data server's file.
md5_validator = True

# Judge data dir
data_dir = path.join( path.dirname(path.dirname(path.abspath(__file__))) , 'Judge_Data' )

# field
META_FIELD = {
    'test-data' : ['.in' , '.out'],
    'md5-check' : ['.in' , '.out'],
    'md5-file' : ['.md5']
}

# Pull data thread lock time out( second )
lock_time_out = 300.0