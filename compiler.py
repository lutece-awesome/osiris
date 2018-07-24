import docker
import settings
from os import path, mkdir
from judge_result import Judge_result

def compile( submission ):
    '''
        Compile the target submission in work_dir
        Return status , info
        if staus eq 'Compile Error' or 'Judger Error' then info would show reasons
        and in any onther cases, the info would be None
    '''
    client = docker.from_env()
    try:
        s = client.containers.run(
            image = settings.docker_repo_arguments.format(
                repo_lang = submission.language.value.image ),
            network_disabled = True,
            volumes = { submission.work_dir : {'bind':  '/opt' , 'mode':'rw' } },
            working_dir = '/opt',
            mem_limit = settings.COMPILE_MEMORY,
            auto_remove = True,
            tty = True,
            detach = True)
        status, info = s.exec_run(
                    cmd = 'timeout ' + str(settings.COMPILE_TIMEOUT) + ' ' + submission.language.value.compile_command.format(
                    sourcefile = submission.sourcefile))
        status = int( status )
        info = info.decode( 'utf-8' )
    finally:
        if 's' in dir():
            s.remove( force = True ) # No matter how this container work, we should remove this container force finally
    if status == 0:
        return 'Success' , None
    elif status is 124:
        info = 'Compile time out'
    elif len( info ) == 0:
        info = 'You wanna hack me? exit code is ' + str( status )
    return Judge_result.CE , info[:min( len(info) , settings.max_compile_error_length )]