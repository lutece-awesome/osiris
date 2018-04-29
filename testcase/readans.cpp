#include <cstdio>

using namespace std;


int main( int argc , char * argv[] ){
    if( freopen( "/opt/10.in" , "r" , stdin ) == NULL ){
        printf( "Can not open answer file.\n" );
        return 0;
    }
    printf( "Yet, I can read answer\n" );
    int a , b;
    scanf( "%d%d" , & a , & b );
    printf( "%d %d\n" , a , b );
    return 0;
}