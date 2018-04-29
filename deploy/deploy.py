import os
import settings
import time

list_dir = list( filter( lambda x: x in settings.Lang , os.listdir() ) )


for i , _ in enumerate( list_dir ):
    running_arguments = 'docker build -t ' + settings.Lang[_] + ' \"' + os.path.join( str( _ ) , '' ) + "\""
    #print( running_arguments )
    os.system( running_arguments )
