import os
import settings

list_dir = list( filter( lambda x: x in settings.Lang , os.listdir() ) )

for _ in list_dir:
    running_arguments = 'docker build -t ' + settings.Lang[_] + ' ' + str( _ ) + '/'
    os.system( running_arguments )
