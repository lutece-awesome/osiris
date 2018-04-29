# compile settings
COMPILE_TIMEOUT = 2.0 # 2.0 seconds
COMPILE_MEMORY = '256mb'

# Judge data dir , this must be same as the story-line file system
data_dir = '/home/xiper/Desktop/Judge_Data'

# Judge work dir
work_dir = '/home/xiper/Desktop/Osiris-Judge-Core/work'

# max error_msg_info, !!do not change this
max_compile_error_length = 480

# set docker repo arguments
docker_repo_arguments = '{repo_lang}'

# set source file name arguments
sourcefile_extension = '{sourcefile}.{extension}'

# set source file running arguments, !!do not change this
sourcefile_running = '{sourcefile}.bin'