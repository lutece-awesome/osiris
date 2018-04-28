#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/time.h>
#include <sys/resource.h>
#include <sys/wait.h>
#include <sys/types.h>
#include <sys/errno.h>
#include <pthread.h>

/*****************************************************************************
 * Run programs on Linux with resource limited.
 * Based on setrlimit.(https://linux.die.net/man/2/setrlimit)
 * Author: Ke Shen
 * Argvs:
    + argv[1]: Time limit(cpu time): milliseconds
    + argv[2]: Memory limit: bytes
    + argv[3]: Output limit: bytes
    + argv[4]: Stack limit: bytes
    + argv[5]: Running arguments
 * EXITCODE:
    + 152 = 24 = CPU TIME EXCEEDED
 *****************************************************************************/
long long timelimit, memorylimit, outputlimit, stacklimit;
int Exceeded_wall_clock_time;
__pid_t pid;

#define errExit( msg ) do{fprintf( stderr , "Core error: %s\n" , msg );exit(-1);}while(0)
#define goodExit( msg ) do{fprintf( stdout , "%s\n" , msg );exit(0);}while(0)

#define set_limit( type , value , ext )                                              \
do{                                                                                  \
    struct rlimit _;                                                                 \
    _.rlim_cur = (value);                                                            \
    _.rlim_max = value + ext;                                                        \
    if ( setrlimit( type , & _ ) != 0 ) {                                            \
        fprintf( stderr , "Setrlimit error(%s): %s\n" , #type , strerror(errno) );   \
        exit( -1 );                                                                  \
    }                                                                                \
}while(0)

void wait_to_kill_childprocess(){
    sleep( ( ( timelimit + 999 ) / 1000 ) + 1 );
    kill( pid , 9 );
    Exceeded_wall_clock_time = 1;
}

int get_status_code( int x ){
    if( x > 128 ) x -= 128;
    return x;
}

int main( int argc , char * argv[] ){
    if( argc != 6 ) errExit( "Arguments number should be 5" );
    timelimit = atoll( argv[1] );
    memorylimit = atoll( argv[2] );
    outputlimit = atoll( argv[3] );
    stacklimit = atoll( argv[4] );
    char * running_arguments = argv[5];
    pid = fork();
    if( pid > 0 ){
        struct rusage result;
        int status;
        pthread_t watch_thread;
        if(pthread_create( & watch_thread , NULL , ( void * )wait_to_kill_childprocess , NULL ))
            errExit( "Can not create watch pthread" );
        wait4( pid , & status , 0 , & result );
        if( status == -1 ) errExit( "Unknown Error" );
        if( status == 127 ) errExit( "Unknown Error" );
        int status_code = get_status_code( WEXITSTATUS(status) );
        long long timecost = ( long long )result.ru_utime.tv_sec * 1000000ll + ( long long )result.ru_utime.tv_usec;
        if( status_code == SIGXCPU || timecost > timelimit * 1000 || Exceeded_wall_clock_time ) goodExit( "Time Limit Exceeded");
        if( status_code == SIGXFSZ ) goodExit( "Output Limit Exceeded" );
        if( result.ru_maxrss > memorylimit ) goodExit( "Memory Limit Exceeded" );
        if( status_code != 0 ) goodExit( "Runtime Error" );
        goodExit( "Success" );
    }else if( pid == 0 ){
        set_limit( RLIMIT_CPU , ( timelimit + 999 ) / 1000 , 1 ); // set cpu_time limit
        set_limit( RLIMIT_AS , memorylimit , ( 1 << 10 ) * (1 << 10) ); // set memory limit
        set_limit( RLIMIT_FSIZE , outputlimit , 0 ); // set output limit
        set_limit( RLIMIT_STACK , stacklimit , 0 ); // set stack limit
        execl( "/bin/sh", "sh", "-c",  running_arguments , (char *) 0);
    }else
        errExit( "Can not fork the child process" );
    return 0;
}