set FORKED_BY_MULTIPROCESSING=1
celery -A tasks worker --loglevel=info -Q task
