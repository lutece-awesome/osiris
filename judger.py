import docker
import compiler
import settings
import language
import os
import time
import sys
import json
from storyline.client.pull import pull , get_case_number
from storyline.client.settings import data_dir
client = docker.from_env()

def modify( submission_id , judge_status , info , case = 0 ):
    pass


def run( submission_id , lang , data_dir , sourcefile , time_limit , memory_limit , checker , case_number ):
    try:
        running_judge_file = 'judge.sh'
        running_core_file = 'core.bin'
        running_checker_file = checker + '.bin'
        running_source_file = sourcefile + '.bin'
        s = client.containers.run(
            image = settings.docker_repo_arguments.format(
                repo_lang = language.get_image( lang ),
            ),
            volumes={ 
            data_dir : {'bind':  '/opt' , 'mode':'rw' }, # mount data
            os.path.join( settings.core_dir , running_judge_file ) : { 'bind': os.path.join( '/home' , running_judge_file ) , 'mode':'rw' }, # mount judge script
            os.path.join( settings.core_dir , running_core_file ) : { 'bind': os.path.join( '/home' , running_core_file ) , 'mode':'rw' }, # mount core
            os.path.join( settings.checker_dir , running_checker_file ) : { 'bind': os.path.join( '/home' , running_checker_file ) , 'mode':'rw' }, # mount checker
            os.path.join( settings.work_dir , running_source_file )  : { 'bind': os.path.join( '/home' , running_source_file ) , 'mode':'rw' }, # mount target program
            },
            network_disabled = True,
            cpuset_cpus = '1', # only 1 cpu core
            working_dir = '/home',  
            tty = True,
            detach = True,
        )
        ret = s.exec_run(
            privileged = True,
            cmd = 'chmod -R 700 /opt' # make user's program can not read answer file
        )
        s.exec_run(
            privileged = True,
            cmd = 'chmod 700 ' + str( running_judge_file ) + ' ' + str( running_core_file ) + ' ' + str( running_checker_file )
        )
        s.exec_run(
            privileged = True,
            cmd = 'chmod 777 ' + str( running_source_file )
        )
    except Exception as e:
        modify( submission_id , 'Judger Error' , str( e ) )
        return
    try:
        ret = s.exec_run(
            privileged = True,
            cmd = settings.shell_script_command.format(
                time_limit = time_limit,
                memory_limit = int(memory_limit) * 1024 * 1024,
                output_limit = 64 * 1024 * 1024, # Default 64mb 
                stack_limit = 64 * 1024 * 1024, # Default 64mb 
                checker = checker,
                running_aruguments = language.get_running_command( lang ).format(
                    sourcefile = sourcefile
                ),
                case_number = case_number,
            ),
            stream = True,
        )
        while True:
            t = ret[1]
            case = 0 
            info = ''
            for _ in t:
                value = _.decode( 'utf-8' )
                dic = json.loads( value )
                case = int( dic['case'] )
                info = dic['info']
                print( case , info )
            modify( 
                submission_id = submission_id,
                judge_status = info[0],
                info = info[1:],
                case = case
            )
            if case == int( case_number ) or info[0] != 'Accepted':
                break
    except Exception as e:
        print( str( e ) )
        modify( submission_id , 'Judger Error' , str( e ) )
    finally:
        if 's' in dir():
            s.remove( force = True )


def judge( submission_id , lang , code , problem , sourcefile , time_limit , memory_limit , checker ):
    if pull( problem ) == False:
        modify( submission_id , 'Judger Error' , 'Can not get/check test-data' )
        exit( 0 )
    st , info = compiler.Compile( 
        lang = lang ,
        code = code ,
        sourcefile = sourcefile)
    if st != 'Success':
        modify( submission_id , st , info )
        exit( 0 )
    data_path = os.path.join( data_dir , str( problem ) )
    run(
        submission_id = submission_id,
        lang = lang ,
        data_dir = data_path,
        sourcefile = sourcefile,
        time_limit = time_limit,
        memory_limit = memory_limit,
        checker = checker,
        case_number = get_case_number( problem )
    )
