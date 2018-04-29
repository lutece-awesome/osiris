import os

# compile settings
COMPILE_TIMEOUT = 2.0 # 2.0 seconds
COMPILE_MEMORY = '256mb'

# set base dir
base_dir = '/home/xiper/Desktop/Osiris-Judge-Core'

# Judge work dir
work_dir = os.path.join( base_dir , 'work' )

# checker dir
checker_dir = os.path.join( base_dir , 'checker' )

# core dir
core_dir = os.path.join( base_dir , 'core' )


# max error_msg_info, !!do not change this
max_compile_error_length = 480

# set docker repo arguments
docker_repo_arguments = '{repo_lang}'

# set source file name arguments
sourcefile_extension = '{sourcefile}.{extension}'

# shell command
shell_script_command = './judge.sh {time_limit} {memory_limit} {output_limit} {stack_limit} {checker} {running_aruguments} {case_number}'