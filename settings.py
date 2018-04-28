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

# set docker repo arguments
docker_repo_arguments = '{CDN_HUB}/{repo_lang}:{repo_tag}'

# set source file name arguments
sourcefile_extension = '{sourcefile}.{extension}'

# set source file running, !!do not change this
sourcefile_running = '{sourcefile}.bin'