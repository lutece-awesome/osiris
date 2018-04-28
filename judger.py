import docker
import compiler
import settings
import language
import os
client = docker.from_env()

def modify( submission_id , judge_status , info ):
    pass



def run( lang , data_dir , sourcefile ):
    sourcefile_running = settings.sourcefile_running.format(
        lang = lang
    )
    s = client.containers.create(
        image = settings.docker_repo_arguments.format(
            CDN_HUB = settings.CDN_HUB_ADDRESS,
            repo_lang = language.get_repo_lang( lang ),
            repo_tag = language.get_repo_tag( lang )
        ),
        volumes={ os.path.join( data_dir ) : {'bind':  '/opt' , 'mode':'ro' } },
        working_dir = '/home',
        command = language.get_compile_command( lang ).format(
            source_file = sourcefile,
            extension = language.get_extension( lang )
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
    pass