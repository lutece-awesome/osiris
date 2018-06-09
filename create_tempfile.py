from os import path, mkdir
from judge_result import Judge_result
import settings

def create_tempfile( sourcefile , lang , code , work_dir ):
    '''
        Create the tempfile in work_dir to save the program
    '''
    if path.isdir( work_dir ) == False:
        mkdir( work_dir )
    try:
        f = open( path.join( work_dir , settings.sourcefile_extension.format(
            sourcefile = sourcefile,
            extension = lang.value.extension
        )) , 'w' )
        f.write( code )
        f.close()
    except Exception as e:
        raise RuntimeError( 'Can not create target file' )
    return 'Success' , None