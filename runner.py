import docker
from os import path
import posixpath
from json import loads
from settings import docker_repo_arguments, core_dir, checker_dir, running_arguments
from update import upload_result
from report.models import Report
from judge_result import Judge_result, get_judge_result
import logging
import tarfile
from io import BytesIO


def set_mode(mode):
    def _set_mode(tarinfo):
        tarinfo.mode = mode
        return tarinfo
    return _set_mode


def run(sub):
    '''
        Run target submission
    '''
    data_dir = '/opt'
    working_dir = '/home'
    try:
        client = docker.from_env()
        running_core_file = 'core.bin'
        running_checker_file = sub.checker + '.bin'
        running_source_file = sub.sourcefile + sub.language.value.running_extension
        upload_result(Report(
            result=Judge_result.RN,
            submission=sub.submission))
        s = client.containers.run(
            image=docker_repo_arguments.format(
                repo_lang=sub.language.value.image),
            volumes={
                sub.data_dir: {'bind':  data_dir, 'mode': 'ro'},
            },
            network_disabled=True,
            # https://docs.docker.com/config/containers/resource_constraints/#cpu
            cpu_period=100000,
            cpu_quota=100000,
            working_dir=working_dir,
            tty=True,
            detach=True,
            auto_remove=True,
        )
        with BytesIO() as tarstream:
            with tarfile.TarFile(fileobj=tarstream, mode='w') as tar:
                tar.add(path.join(core_dir, running_core_file),
                        running_core_file, filter=set_mode(0o700))
                tar.add(path.join(checker_dir, running_checker_file),
                        running_checker_file, filter=set_mode(0o700))
                tar.add(path.join(sub.work_dir, running_source_file),
                        running_source_file, filter=set_mode(0o777))
            tarstream.seek(0)
            s.put_archive(working_dir, tarstream)
        for i, x in enumerate(sub.case):
            running_command = running_arguments.format(
                time_limit=sub.time_limit,
                memory_limit=sub.memory_limit * 1024 * 1024,
                output_limit=sub.output_limit * 1024 * 1024,
                stack_limit=sub.stack_limit * 1024 * 1024,
                input_sourcefile=posixpath.join(data_dir, x[0]),
                output_sourcefile='user.out',
                answer_sourcefile=posixpath.join(data_dir, x[1]),
                running_arguments=sub.language.value.running_command.format(
                    sourcefile=sub.sourcefile),
                checker_sourcefile=sub.checker)
            ret = s.exec_run(cmd=running_command)
            logging.info("exit code: %s, output: %s",
                         ret[0], ret[1].decode('utf-8'))
            exit_code, output = int(ret[0]), loads(ret[1].decode('utf-8'))
            output['result'] = get_judge_result(output['result'])
            output['case'] = i + 1
            output['submission'] = sub.submission
            if output['result'] is Judge_result.AC and i != len(sub.case) - 1:
                output['complete'] = False
            else:
                output['complete'] = True
            upload_result(report=Report(** output))
            if output['result'] is not Judge_result.AC:
                break
    except Exception as e:
        raise RuntimeError("Judger Error during running: " + str(e))
    finally:
        if 's' in dir():
            s.remove(force=True)
