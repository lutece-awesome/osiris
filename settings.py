# HTTP or HTTPS?
protocol = 'http://'
# PORT
PORT = '8000'
# Server ip address
web_server_ip = '127.0.0.1'
# fetch url
fetch_submission_url =  protocol + web_server_ip + ':' + PORT + '/' + 'submission/fetch/judge'

# set cdn_hub address
CDN_HUB_ADDRESS = 'registry.docker-cn.com/library'

# compile 
COMPILE_TIMEOUT = 2.0 # 2.0 seconds
COMPILE_MEMORY = '256mb'

# Judge data dir , this must be same as the story-line file system
data_dir = '/home/xiper/Desktop/Judge_Data'

# Judge work dir
work_dir = '/home/xiper/Desktop/Osiris-Judge-Core/work'

# max error_msg_info, !!do not change this
max_compile_error_length = 480