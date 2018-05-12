from os import path, getcwd

# process number of judge, eq the cpu cores is better
MAX_JUDGE_PROCESS = 4

# compile settings
COMPILE_TIMEOUT = 2.0 # 2.0 seconds
COMPILE_MEMORY = '256mb'

# set base dir
base_dir = path.dirname(path.abspath(__file__))

# Judge work dir, do not change this
base_work_dir = path.join( base_dir , 'work' )

# checker dir, do not change this
checker_dir = path.join( base_dir , 'checker' )

# core dir, do not change this
core_dir = path.join( base_dir , 'core' )

# max error_msg_info, do not change this
max_compile_error_length = 480

# set docker repo arguments
docker_repo_arguments = '{repo_lang}'

# set source file name arguments
sourcefile_extension = '{sourcefile}.{extension}'

# running arguments
running_arguments = './core.bin {time_limit} {memory_limit} {output_limit} {stack_limit}     \
                    \"{input_sourcefile}\" \"{output_sourcefile}\" \"{answer_sourcefile}\"   \
                    \"{running_arguments}\" \"{checker_sourcefile}\"'

                    
