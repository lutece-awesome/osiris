import socket
from . import sync, settings
import pickle
import time
import os
import hashlib

def read_header_length( msg ):
    header_length = 0
    for _ in range( 0 , settings.header_length ):
        header_length = ( header_length << 1 ) + int( msg[_] ) - ord( '0' )
    return header_length + settings.header_length

def recv_data( soc ):
    msg = []
    curlen = 0
    maxlength = -1
    while True:
        data = soc.recv( settings.buffersize )
        msg.append( data )
        curlen += len( data )
        if curlen >= settings.header_length and maxlength == -1:
            maxlength = read_header_length( ( b''.join( msg ) ) )
        if curlen == maxlength:
            break
    msg = b''.join( msg )
    return pickle.loads( msg[settings.header_length:] )
    
def send_data( soc , data ):
    length = len( data )
    header_str = ''
    for _ in range( 0 , settings.header_length ):
        header_str += str( length & 1 )
        length >>= 1
    header_str = header_str[::-1]
    soc.sendall( header_str.encode( 'ascii' ) + data )


def pull_data( problem , data_type ):
    '''
        pull the problem's data from data server.
        The choice of data_type can be one of the settings.META_TYPE
    '''
    msg = {
        'problem' : problem,
        'type' : data_type,
    }
    try:
        s = socket.socket( socket.AF_INET , socket.SOCK_STREAM )
        s.settimeout( settings.time_out )
        s.connect( ( settings.data_server , settings.port ) )
        send_data( s , pickle.dumps( msg , 2 ) )
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
    except:
        return False
    return True

def pull( problem ):
    '''
        Pull the problem from data_server
        If pull success return True otherwise return False
    '''
    if settings.md5_validator == True and check_cache( problem ):
        return True
    recv = pull_data( problem , 'test-data' )
    if recv == None or sync.rewrite( problem , recv) == False:
        return False
    return True

def get_case_number( problem ):
    list_dir = os.listdir( os.path.join( settings.data_dir , str( problem ) ) )
    return len( list( filter( lambda x : os.path.splitext( x )[1] == '.in' , list_dir ) ) )

def get_data_dir( problem ):
    return os.path.join( settings.data_dir , str( problem ) )