import docker
import compiler
import settings
import language
import os
client = docker.from_env()

def modify( submission_id , judge_status , info ):
    pass



def run( lang , data_dir , sourcefile , time_limit ):
    shell_file_content = language.running_shell_arguments.format(
        time_limit = time_limit,
        memory_limit = memory_limit,
        output_limit = output_limit,
        stack_limit = stack_limit,
        checker = checker,
        running_core = 'core',
        sourcefile = sourcefile,
        data_dir = data_dir,
        case_number = case_number,
    )

    sourcefile_running = settings.sourcefile_running.format(
        lang = lang
    )
    s = client.containers.create(
        image = settings.docker_repo_arguments.format(
            repo_lang = language.get_image( lang ),
        ),
        volumes={ os.path.join( data_dir ) : {'bind':  '/opt' , 'mode':'ro' } },
        working_dir = '/home',
        command = language.get_running_command( lang ).format(
            sourcefile = sourcefile
        ),
        auto_remove = False,
    )
    pass



def judge( submission_id , lang , code , problem , sourcefile ):
    st , info = compiler.Compile( 
        lang = lang ,
        code = code ,
        sourcefile = sourcefile)
    if st != 'Success':
        modify( submission_id , st , info )
    run( 
        lang = lang , 
        data_dir = os.path.join( settings.data_dir , str( problem ) ) ,  
        sourcefile = sourcefile
    )
    pass