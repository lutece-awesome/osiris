from celery import Celery
from multiprocessing import current_process
from settings import base_work_dir
from judger import judge_submission
from submission.models import Submission
from submission_parser import parse
from os import path
from util.problem_locker import gloal_problem_lock
from judge_result import Judge_result
import logging

app = Celery(name='task')
app.config_from_object('celeryconfig')


@app.task(name='Judger.task')
def get_submission_task(submission):
    name = current_process().name
    try:
        submission = parse(**submission)
        sub = Submission(**{**submission, **{
            'work_dir': path.join(base_work_dir, name),
            'output_limit': 64,
            'stack_limit': 64,
            'sourcefile': 'Main'}})
        logging.info('%s got submission, start judging(%s)',
                     name, sub.submission)
        judge_submission(sub)
    except Exception as e:
        from update import upload_result
        from report.models import Report
        upload_result(Report(
            result=Judge_result.JE,
            complete=True,
            submission=sub.submission,
            judgererror_msg=str(e)))
        logging.error('%s error happen: %s', name, e)


@app.task(name='Judger.result')
def upload_result_into_queue(report):
    pass
