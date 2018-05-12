from os import path, system, mkdir
from . settings import data_dir

def sync( problem ):
    try:
        dr = path.join( data_dir , str( problem ) )
        system( 'rm ' + path.join( dr , '*' ) )
    except:
        return False
    return True

def rewrite( problem , msg ):
    try:
        dr = path.join( data_dir , str( problem ) )
        if path.exists( dr ) == False:
            mkdir( dr )
        for _ in msg:
            f = open( path.join( dr , str( _ ) ) , "wb" )
            f.write( msg[_] )
            f.close()
    except:
        return False
    return True
