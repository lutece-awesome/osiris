import os
import posixpath
from settings import Language


for each_lang in Language:
    running_arguments = 'docker build -t ' + each_lang.value.image + ' \"' + posixpath.join( each_lang.value.file , '' ) + "\""
    os.system( running_arguments )
