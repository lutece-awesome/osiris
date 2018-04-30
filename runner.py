import docker
from os import path
from settings import docker_repo_arguments, core_dir, checker_dir, work_dir
from language import get_image

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
    # make user's program can not read answer file
    s.exec_run( privileged = True , cmd = 'chmod -R 700 /opt' )
    s.exec_run( privileged = True , cmd = 'chmod 700 ' + str( running_core_file ) + ' ' + str( running_checker_file ))
    s.exec_run( privileged = True , cmd = 'chmod 777 ' + str( running_source_file ) )
    for i in range( 1 , submission.case_number + 1 ):
        pass
    s.remove( force = True )
