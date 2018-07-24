from os import path, system, mkdir, chmod
from . settings import data_dir


def sync(problem):
    try:
        dr = path.join(data_dir, str(problem))
        system('rm ' + path.join(dr, '*'))
    except:
        return False
    return True


def rewrite(problem, msg):
    try:
        sync(problem)
        dr = path.join(data_dir, str(problem))
        if not path.exists(dr):
            mkdir(dr, 0o700)
        for filename in msg:
            with open(path.join(dr, filename), "wb") as f:
                f.write(msg[filename])
            chmod(path.join(dr, filename), 0o700)
    except:
        return False
    return True
