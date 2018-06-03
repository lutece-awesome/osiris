import os
from settings import Language


for each_lang in Language:
    running_arguments = 'docker build -t ' + each_lang.value.image + ' \"' + os.path.join( each_lang.value.file , '' ) + "\""
    os.system( running_arguments )
