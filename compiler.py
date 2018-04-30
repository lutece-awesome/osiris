import docker
import language
import settings
from os import path

def create_tempfile( sourcefile , lang , code ):
    '''
        Create the tempfile in work_dir to save the program
    '''
    if lang not in language.SUPPORT_LANGUAGE:
        return 'Compile Error' , 'Unsupported Language'
    try:
        f = open( path.join(settings.work_dir , settings.sourcefile_extension.format(
            sourcefile = sourcefile,
            extension = language.get_extension( lang )
        ))   
        , 'w' )
        f.write( code )
        f.close()
    except:
        return 'Judger Error' , 'Can not create target file'
    return 'Success' , None

def compile( submission ):
    '''
        Compile the target submission in work_dir
        Return status , info
        if staus eq 'Compile Error' or 'Judger Error' then info would show reasons
        and in any onther cases, the info would be None
    '''
    st , info = create_tempfile( 
        sourcefile = submission.sourcefile,
        lang = submission.language,
        code = submission.code
    )
    client = docker.from_env()
    if st != 'Success':
        return st , info
    try:
        running_source_file = settings.sourcefile_extension.format(
            sourcefile = submission.sourcefile,
            extension = language.get_extension( submission.language ))
        s = client.containers.run(
            image = settings.docker_repo_arguments.format(
                repo_lang = language.get_image( submission.language )),
            network_disabled = True,
            volumes = { path.join( settings.base_dir , settings.work_dir ) : {'bind':  '/opt' , 'mode':'rw' } },
            working_dir = '/opt',
            mem_limit = settings.COMPILE_MEMORY,
            auto_remove = False,
            tty = True,
            detach = True)
        status, info = s.exec_run(
                    privileged = True,
                    cmd = 'timeout ' + str(settings.COMPILE_TIMEOUT) + ' ' + language.get_compile_command( submission.language ).format(
                    sourcefile = submission.sourcefile,
                    extension = language.get_extension( submission.language )))
        status = int( status )
        info = info.decode( 'utf-8' )
    except Exception as e:
        return 'Judger Error' , str( e )
    finally:
        if 's' in dir():
            s.remove( force = True ) # No matter how this container work, we should remove this container force finally
    if status == 0:
        return 'Success' , None
    return 'Compile Error' , info[:min( len(info) , settings.max_compile_error_length )]