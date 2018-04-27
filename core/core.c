#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/time.h>
#include <sys/resource.h>
/*****************************************************************************
 * Run programs on Linux with resource limited.
 * Based on setrlimit.(https://linux.die.net/man/2/setrlimit)
 * Argvs:
    + argv[1]: Time limit(cpu time): 2000
    + argv[2]: Memory Limit
 *****************************************************************************/

int fib(int n) {
    if(n<=1) return 1;
    return fib(n-1)+fib(n-2);
}

int main( int argc , char * argv[] ){
    //int timelimit = atoi(argv[1]);

    //int memorylimit = atoi(argv[2]);

    /*

    int pid = fork();
    if( pid > 0 ){

    }else if( pid == 0 ){
        printf( "time limit is %d\n" , timelimit );
        printf( "this is child process.\n" );
        // limit time
        if( timelimit >= 0 ){
            struct rlimit _;
            _.rlim_cur = 2.5;
            _.rlim_max = 2.5;
            setrlimit( RLIMIT_CPU , & _ );
        }else
            return -2;
        
    }else
        return -1;
    */
    return 0;
}