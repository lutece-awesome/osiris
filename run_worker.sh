TASK_QUEUE=task

celery -A tasks worker -c 1 --loglevel=info -Q $TASK_QUEUE
