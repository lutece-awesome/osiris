from listen import process , read_header_length
import time

#process( None , 1 , 'md5' )
s = read_header_length( b'0000000000000000000000000000000000000000000000000000000000111001\x80\x02}q\x00(X\x07\x00\x00\x00problemq\x01X\x01\x00\x00\x001q\x02X\x04\x00\x00\x00typeq\x03X\t\x00\x00\x00test-dataq\x04u.' )
print( s )