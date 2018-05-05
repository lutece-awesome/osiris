import socket , os , hashlib , settings
from . import sync
from pickle import dumps
from . problem_locker import gloal_problem_lock

def pull_data( problem , data_type ):
    '''
        pull the problem's data from data server.
        The choice of data_type can be one of the settings.META_TYPE
    '''
    msg = {
        'problem' : problem,
        'type' : data_type}
    try:
        s = socket.socket( socket.AF_INET , socket.SOCK_STREAM )
        s.settimeout( settings.time_out )
        s.connect( ( settings.data_server , settings.port ) )
        send_data( s , dumps( msg , 2 ) )
        ret = recv_data( s )
        s.close()
    except:
        return None
    return ret

def cal_md5_or_create( problem , force = False ):
    '''
        Calcuate the md5-field of problem folder
        if force is True, always create/update md5 file
    '''
    try:
        path = os.path.join( settings.data_dir , str( problem ) )
        li = os.listdir( path )
        if 'md5' in li and force is False:
            return True
        li = list( filter( lambda x : os.path.splitext( x )[1] in settings.META_FIELD['md5'] , li ) )
        kwargs = []
        for _ in li:
            f = open( os.path.join( path , _ ) , "rb" )
            md5 = hashlib.md5()
            md5.update( f.read() )
            content = md5.hexdigest()
            f.close()
            kwargs.append( ( _ , content ) )
        kwargs.sort()
        f = open( os.path.join( path , 'md5' ) , "w" )
        f.write( str( kwargs ) )
        f.close()
    except Exception as e:
        return False , str( e )
    return True

def check_cache( problem ):
    '''
        Check cache
    '''
    try:
        recv = pull_data( problem , 'md5' )
        if recv is None:
            return False
        cal_md5_or_create( problem )
        recv.sort()
        if recv != open( os.path.join( settings.data_dir , str( problem ) ) ).read():
            return False
    except:
        return False
    return True

def pull( lock , problem ):
    '''
        Pull the problem from data_server
        If pull success return True otherwise return False and reasons
    '''
    lock.acquire()
    try:
        if settings.md5_validator == True and check_cache( problem ):
            return True , None
        recv = pull_data( problem , 'test-data' )
        if recv == None or sync.rewrite( problem , recv) == False:
            return False , 'can not recv data or rewrite data to disk'
        return True , None
    except RuntimeError:
        return False , 'Pull-data time out'
    except Exception as e:
        return False , str( e )
    finally:
        lock.release()

def get_case_number( problem ):
    list_dir = os.listdir( os.path.join( settings.data_dir , str( problem ) ) )
    return len( list( filter( lambda x : os.path.splitext( x )[1] == '.in' , list_dir ) ) )

def get_data_dir( problem ):
    return os.path.join( settings.data_dir , str( problem ) )