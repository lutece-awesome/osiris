import socket
from . import sync, settings
from pickle import dumps
import os
import hashlib
from problem_locker import gloal_problem_lock

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

def check_cache( problem ):
    try:
        recv = pull_data( problem , 'md5' )
        path = os.path.join( settings.data_dir , str( problem ) )
        li = os.listdir( path )
        if len( li ) != len( recv ):
            return False
        for _ in li:
            if _ not in recv:
                return False
            f = open( os.path.join( path , _ ) , "rb" )
            md5 = hashlib.md5()
            md5.update( f.read() )
            content = md5.hexdigest()
            if content != recv[_]:
                return False
            f.close()
    except:
        return False
    return True

def pull( problem ):
    '''
        Pull the problem from data_server
        If pull success return True otherwise return False
    '''
    gloal_problem_lock.get( problem ).acquire( timeout = settings.lock_time_out )
    try:
        if settings.md5_validator == True and check_cache( problem ):
            return True , None
        recv = pull_data( problem , 'test-data' )
        if recv == None or sync.rewrite( problem , recv) == False:
            return False , 'can not recv data or rewrite data to disk'
        return True , None
    except RuntimeError:
        return False , 'Pull-data time out'
    except:
        return False , str( e )
    finally:
        gloal_problem_lock.get( problem ).release()
    


def get_case_number( problem ):
    list_dir = os.listdir( os.path.join( settings.data_dir , str( problem ) ) )
    return len( list( filter( lambda x : os.path.splitext( x )[1] == '.in' , list_dir ) ) )


def get_data_dir( problem ):
    return os.path.join( settings.data_dir , str( problem ) )