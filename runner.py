import docker
from os import path
from json import loads
from settings import docker_repo_arguments, core_dir, checker_dir, work_dir, running_arguments
from language import get_image, get_running_command
from util.update import upload_result
from report.models import Report

def run( submission ):
    '''
        Run target submission
    '''
    client = docker.from_env()
    running_core_file = 'core.bin'
    running_checker_file = submission.checker + '.bin'
    running_source_file = submission.sourcefile + '.bin'
    s = client.containers.run(
        image = docker_repo_arguments.format(
            repo_lang = get_image( submission.language ),),
        volumes={
            submission.data_dir : {'bind':  '/opt' , 'mode':'rw' }, # mount data
            path.join( core_dir , running_core_file ) : { 'bind': path.join( '/home' , running_core_file ) , 'mode':'rw' }, # mount core
            path.join( checker_dir , running_checker_file ) : { 'bind': path.join( '/home' , running_checker_file ) , 'mode':'rw' }, # mount checker
            path.join( work_dir , running_source_file )  : { 'bind': path.join( '/home' , running_source_file ) , 'mode':'rw' }}, # mount target program},
        network_disabled = True,
        cpuset_cpus = '1',
        working_dir = '/home',
        tty = True,
        detach = True)
    try:
        # make user's program can not read answer file
        s.exec_run( privileged = True , cmd = 'chmod -R 700 /opt' )
        s.exec_run( privileged = True , cmd = 'chmod 700 ' + str( running_core_file ) + ' ' + str( running_checker_file ))
        s.exec_run( privileged = True , cmd = 'chmod 777 ' + str( running_source_file ) )
        for i in range( 1 , submission.case_number + 1 ):
            upload_result( report = Report( result = 'Running' , case = i ) )
            running_command = running_arguments.format(
                time_limit = submission.time_limit,
                memory_limit = submission.memory_limit * 1024 * 1024,
                output_limit = submission.output_limit * 1024 * 1024,
                stack_limit = submission.stack_limit * 1024 * 1024,
                input_sourcefile = path.join( '/opt' , str( i ) + '.in' ),
                output_sourcefile = 'user.out',
                answer_sourcefile = path.join( '/opt' , str( i ) + '.out' ),
                running_arguments = get_running_command( submission.language ).format( sourcefile = submission.sourcefile ),
                checker_sourcefile = submission.checker)
            ret = s.exec_run(
                privileged = True,
                cmd = running_command )
            exit_code , output = int( ret[0] ) , loads( ret[1].decode( 'utf-8' ) )
            output['case'] = i
            upload_result( report = Report( ** output ) )
            if output['result'] != 'Accepted':
                break
    finally:
        s.remove( force = True )