export PYTHONOPTIMIZE=1
export PYTHONOPTIMIZE=1 #(https://github.com/celery/celery/issues/1709)
celery -A osiris worker --loglevel=info -c 1