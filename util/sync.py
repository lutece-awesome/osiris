import os , settings

def sync( problem ):
    try:
        path = os.path.join( settings.data_dir , str( problem ) )
        os.system( 'rm ' + os.path.join( path , '*' ) )
    except:
        return False
    return True

def rewrite( problem , msg ):
    try:
        path = os.path.join( settings.data_dir , str( problem ) )
        for _ in msg:
            f = open( os.path.join( path , str( _ ) ) , "wb" )
            f.write( msg[_] )
            f.close()
    except:
        return False
    return True
