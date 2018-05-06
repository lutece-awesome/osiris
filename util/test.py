from requests import get
from pickle import dumps, loads
from time import clock
from os import path

def request_problem( problem ):
    st = clock()
    ret = get( url = 'http://127.0.0.1:8000/data_server/fetch/2' )
    text = loads( ret.content ) 
    for _ in text:
        f = open( path.join( '/home/xiper/Desktop/Judge_Data/2' , _  ) , "wb" )
        f.write( text[_] )
        f.close()
    print( 'time cost' , clock() - st )


request_problem( 2 )