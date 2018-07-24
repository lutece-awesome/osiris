from os import path, mkdir
from judge_result import Judge_result
import settings


def create_tempfile(sourcefile, lang, code, work_dir):
    '''
        Create the tempfile in work_dir to save the program
    '''
    if not path.isdir(work_dir):
        mkdir(work_dir)
    try:
        with open(path.join(work_dir, settings.sourcefile_extension.format(
                sourcefile=sourcefile,
                extension=lang.value.extension)), 'w') as f:
            f.write(code)
    except Exception as e:
        raise RuntimeError('Can not create target file')
    return 'Success', None
