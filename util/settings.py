# HTTP or HTTPS?
protocol = 'http://'
# PORT
PORT = '8000'
# Server ip address
web_server_ip = '127.0.0.1'
# fetch url
fetch_submission_url =  protocol + web_server_ip + ':' + PORT + '/submission/fetch/judge'
# modify url
modify_submission_url = protocol + web_server_ip + ':' + PORT + '/submission/modify/judge/'

# md5_validator is to check whether the local file equals the data server's file.
md5_validator = True

# client's settings
data_server = '127.0.0.1'

# port
port = 6100

# buffsize
buffersize = 8192

# Judge data dir
data_dir = '/home/xiper/Desktop/Judge_Data'

# field
META_FIELD = {
    'test-data' : ['.in' , '.out'],
    'md5' : ['.in' , '.out'],
}

# header , only include length
header_length = 64

# socket time_out( second )
time_out = 60.0

# Pull data thread lock time out( second )
lock_time_out = 60.0