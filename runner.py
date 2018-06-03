import docker
from os import path
from json import loads
from settings import docker_repo_arguments, core_dir, checker_dir, running_arguments
from update import upload_result
from report.models import Report
from judge_result import Judge_result, get_judge_result

def run( sub ):
    '''
        Run target submission
    '''
    client = docker.from_env()
    running_core_file = 'core.bin'
    running_checker_file = sub.checker + '.bin'
    running_source_file = sub.sourcefile + sub.language.value.running_extension
    upload_result( Report(
        result = Judge_result.RN,
        submission = sub.submission ))
    s = client.containers.run(
        image = docker_repo_arguments.format(
            repo_lang = sub.language.value.image),
        volumes={
            sub.data_dir : {'bind':  '/opt' , 'mode':'rw' }, # mount data
            path.join( core_dir , running_core_file ) : { 'bind': path.join( '/home' , running_core_file ) , 'mode':'rw' }, # mount core
            path.join( checker_dir , running_checker_file ) : { 'bind': path.join( '/home' , running_checker_file ) , 'mode':'rw' }, # mount checker
            path.join( sub.work_dir , running_source_file )  : { 'bind': path.join( '/home' , running_source_file ) , 'mode':'rw' }}, # mount target program},
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
        for i , x in enumerate( sub.case ):
            running_command = running_arguments.format(
                time_limit = sub.time_limit,
                memory_limit = sub.memory_limit * 1024 * 1024,
                output_limit = sub.output_limit * 1024 * 1024,
                stack_limit = sub.stack_limit * 1024 * 1024,
                input_sourcefile = path.join( '/opt' , x[0] ),
                output_sourcefile = 'user.out',
                answer_sourcefile = path.join( '/opt' , x[1] ),
                running_arguments = sub.language.value.running_command.format( sourcefile = sub.sourcefile ),
                checker_sourcefile = sub.checker)
            ret = s.exec_run(
                privileged = True,
                cmd = running_command )
            exit_code , output = int( ret[0] ) , loads( ret[1].decode( 'utf-8' ) )
            output['result'] = get_judge_result( output['result'] )
            output['case'] = i + 1
            output['submission'] = sub.submission
            if output['result'] is Judge_result.AC and i != len( sub.case ) - 1:
                output['complete'] = False
            else:
                output['complete'] = True
            upload_result( report = Report( ** output ) )
            if output['result'] is not Judge_result.AC:
                break
    finally:
        s.remove( force = True )