

# lutece settings
FETCH_SUBMISSION_ADDR = '127.0.0.1'
FETCH_SUBMISSION_PORT = 6106
FETCH_SUBMISSION_AUTHKEY = b'772002' # in producing envir, this should be sercet
FETCH_DATA_URL =  'http://' + FETCH_SUBMISSION_ADDR + ':8000' + '/data_server/fetch/'

# md5_validator is to check whether the local file equals the data server's file.
md5_validator = True

# Judge data dir
data_dir = '/home/xiper/Desktop/Judge_Data'

# field
META_FIELD = {
    'test-data' : ['.in' , '.out'],
    'md5-check' : ['.in' , '.out'],
    'md5-file' : ['.md5']
}

# Pull data thread lock time out( second )
lock_time_out = 60.0