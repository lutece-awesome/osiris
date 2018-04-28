from pull import pull , send_data , check_cache
from sync import sync
import time

s = time.clock()
#sync( 1 )
pull( '1' )
#print( check_cache( 1 ) )
print( 'Time Cost: ' , time.clock() - s )