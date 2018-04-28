import socket , pickle
import settings
import logging
import os
import hashlib
import time
logging.basicConfig(level=logging.INFO)

def read_header_length( msg ):
    header_length = 0
    for _ in range( 0 , settings.header_length ):
        header_length = ( header_length << 1 ) + int( msg[_] ) - ord( '0' )
    return header_length + settings.header_length

def recv_data( soc ):
    msg = b''
    curlen = 0
    maxlength = -1
    while True:
        data = soc.recv( settings.buffersize )
        msg += data
        curlen += len( data )
        if curlen >= settings.header_length and maxlength == -1:
            maxlength = read_header_length( msg )
        if curlen == maxlength:
            break
    return pickle.loads( msg[settings.header_length:] )
    
def send_data( soc , data ):
    length = len( data )
    header_str = ''
    for _ in range( 0 , settings.header_length ):
        header_str += str( length & 1 )
        length >>= 1
    header_str = header_str[::-1]
    soc.sendall( header_str.encode( 'ascii' ) + data )


def process( soc , problem , data_type ):
    try:
        path = os.path.join( settings.data_dir , str( problem ) )
        li = list(filter( lambda x: os.path.splitext(x)[1] in settings.META_FIELD[data_type] , os.listdir( path ) ))
        li.sort()
        rcv = {}
        for _ in li:
            f = open( os.path.join( path , _ ) , "rb" )
            content = f.read()
            if data_type == 'md5':
                md5 = hashlib.md5()
                md5.update( content )
                content = md5.hexdigest()
            rcv[_] = content
            f.close()
        send_data( soc , pickle.dumps( rcv , 2 ) )
    except:
        return False
    return True

def run_storyline_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = '127.0.0.1'
    s.bind( ( ip , settings.port ) )  
    s.listen( settings.max_connection )
    logging.info( 'Storyline start completed, now listen ' + str(ip) + ':' + str(settings.port) )
    while True:
        soc , add = s.accept()
        logging.info( 'Listen ' + str( add ) )
        try:
            js = recv_data( soc )
            process( soc , js['problem'] , js['type']  )
        finally:
            logging.info( 'Close ' + str( add ))
            soc.close()
