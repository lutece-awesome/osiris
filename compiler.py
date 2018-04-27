import docker
from language import SUPPORT_LANGUAGE
import settings
import time
import os
import sys

docker_repo_arguments = '{CDN_HUB}/{lang}:{tag}'
source_file_name = 'main-{thread}.{extension}'
client = docker.from_env()

def create_tempfile( thread_id , lang , code ):
    if lang not in SUPPORT_LANGUAGE:
        return 'Unsupported Language'
    try:
        f = open( os.path.join(settings.work_dir , source_file_name.format(
            thread = thread_id,
            extension = SUPPORT_LANGUAGE[lang]['extension']
        ))   
        , 'w' )
        f.write( code )
    except:
        return 'Judger Error' , None
    return 'Success' , 'main-' + str( thread_id )

def Compile( lang , code ,  thread_id ):
    st , sourcefile = create_tempfile( 
        thread_id = thread_id ,
        lang = lang,
        code = code
    )
    if st != 'Success':
        return st , None
    try:
        s = client.containers.create(
            image = docker_repo_arguments.format(
                CDN_HUB = settings.CDN_HUB_ADDRESS,
                lang = SUPPORT_LANGUAGE[lang]['docker_repo'],
                tag = SUPPORT_LANGUAGE[lang]['docker_repo_tag'],
                mem_limit = settings.COMPILE_MEMORY,
            ),
            volumes={ os.path.join( settings.work_dir ) : {'bind':  '/opt' , 'mode':'rw' } },
            working_dir = '/opt',
            command = SUPPORT_LANGUAGE[lang]['compile_command'].format(
                source_file = sourcefile,
                extension = SUPPORT_LANGUAGE[lang]['extension'],
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
