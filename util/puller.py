import hashlib
from pickle import loads as pickle_loads
from json import dumps as json_dumps
from .settings import META_FIELD, data_dir, md5_validator, FETCH_SUBMISSION_AUTHKEY, FETCH_DATA_URL, lock_time_out
from .sync import rewrite
from requests import post
from os import path , listdir

def get_data( problem , data_type ):
    '''
        get data of data_type
    '''
    dr = path.join( data_dir , str( problem ) )
    li = list(filter( lambda x: path.splitext(x)[1] in META_FIELD[data_type] , listdir( dr ) ) )
    li.sort()
    _send = {}
    for _ in li:
        f = open( path.join( dr , _ ) , "rb" )
        _send[_] = f.read()
        f.close()
    return _send

def pull_data( problem , data_type ):
    '''
        pull the problem's data from data server.
        The choice of data_type can be one of the settings.META_TYPE
    '''
    msg = {
        'problem' : problem,
        'type' : data_type,
        'authkey' : FETCH_SUBMISSION_AUTHKEY }
    try:
        r = post(
            url = FETCH_DATA_URL,
            data = msg )
        return pickle_loads( r.content )
    except Exception as e:
        return None

def cal_md5_or_create( problem , force = False ):
    '''
        Calcuate the md5-field of problem folder
        if force is True, always create/update md5 file
    '''
    try:
        dr = path.join( data_dir , str( problem ) )
        li = listdir( dr )
        if 'data.md5' in li and force is False:
            return True , None
        li = list( filter( lambda x : path.splitext( x )[1] in META_FIELD['md5-check'] , li ) )
        args = []
        for _ in li:
            f = open( path.join( dr , _ ) , "rb" )
            md5 = hashlib.md5()
            md5.update( f.read() )
            content = md5.hexdigest()
            f.close()
            args.append( ( _ , content ) )
        args.sort()
        f = open( path.join( dr , 'data.md5' ) , "w" )
        f.write( str( args ) )
        f.close()
    except Exception as e:
        return False , str( e )
    return True , None


def check_cache( problem ):
    '''
        Check cache
    '''
    try:
        recv = pull_data( problem , 'md5-file' )
        if recv is None:
            return False
        cal_md5_or_create( problem )
        if recv != get_data( problem , 'md5-file' ):
            return False
    except Exception as e:
        return False
    return True


def pull( lock , problem ):
    '''
        Pull the problem from data_server
        If pull success return True otherwise return False and reasons
    '''
    lock.acquire( timeout = lock_time_out )
    try:
        if md5_validator == True and check_cache( problem ):
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
    list_dir = listdir( path.join( data_dir , str( problem ) ) )
    return len( list( filter( lambda x : path.splitext( x )[1] == '.in' , list_dir ) ) )

def get_data_dir( problem ):
    return path.join( data_dir , str( problem ) )