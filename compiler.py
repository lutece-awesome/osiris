import docker
import language
import settings
import time
import os
import sys

client = docker.from_env()

def create_tempfile( sourcefile , lang , code ):
    if lang not in language.SUPPORT_LANGUAGE:
        return 'Compile Error' , 'Unsupported Language'
    try:
        f = open( os.path.join(settings.work_dir , settings.sourcefile_extension.format(
            sourcefile = sourcefile,
            extension = language.get_extension( lang )
        ))   
        , 'w' )
        f.write( code )
    except:
        return 'Judger Error' , 'Can not create target file'
    return 'Success' , None

def Compile( lang , code , sourcefile ):
    st , info = create_tempfile( 
        sourcefile = sourcefile ,
        lang = lang,
        code = code
    )
    if st != 'Success':
        return st , info
    try:
        s = client.containers.create(
            image = settings.docker_repo_arguments.format(
                CDN_HUB = settings.CDN_HUB_ADDRESS,
                repo_lang = language.get_repo_lang( lang ),
                repo_tag = language.get_repo_tag( lang )
            ),
            mem_limit = settings.COMPILE_MEMORY,
            volumes={ os.path.join( settings.work_dir ) : {'bind':  '/opt' , 'mode':'rw' } },
            working_dir = '/opt',
            command = language.get_compile_command( lang ).format(
                source_file = sourcefile,
                extension = language.get_extension( lang )
            ),
            auto_remove = False,
        )
        s.start()
        ret = s.wait(
            timeout = settings.COMPILE_TIMEOUT
        )
    except Exception as e:
        return 'Compile Error' , str(e)
    finally:
        if 's' in dir():
            compile_info_msg = s.logs()[:min( len(s.logs()) , settings.max_compile_error_length )]
            s.remove( force = True ) # No matter how this container work, we should remove this container force finally
    if ret['StatusCode'] == 0:
        return 'Success' , None
    return 'Compile Error' , compile_info_msg.decode( 'utf-8' )
