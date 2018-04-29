#include <cstdio>
#include <unistd.h>

using namespace std;


int main( int argc , char * argv[] ){
    sleep( 4 );
    int a , b;
    scanf( "%d%d" , & a , & b );
    printf( "%d\n" , a + b );
    return 0;
}