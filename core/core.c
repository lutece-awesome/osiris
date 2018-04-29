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
    + argv[5]: Input sourcefile
    + argv[6]: Output sourcefile
    + argv[7]: Answer sourcefile
    + argv[8]: Running sourcefile
    + argv[9]: Checker sourcefile
 * EXITCODE:
    + 152 = 24 = CPU TIME EXCEEDED
 *****************************************************************************/
long long timelimit, memorylimit, outputlimit, stacklimit;
int Exceeded_wall_clock_time;
char checker_arguments[666] , running_arguments[666];
__pid_t pid;
char * input_sourcefile , * output_sourcefile , * answer_sourcefile , * running_sourcefile , * checker_sourcefile;


#define errExit( msg ) do{fprintf( stdout , "Core error: %s\n" , msg );exit(-1);}while(0)
#define goodExit( msg , timecost , memorycost ) do{fprintf( stdout , "%s %lld %ld\n" , msg , timecost , memorycost );exit(0);}while(0)

#define set_limit( type , value , ext )                                              \
do{                                                                                  \
    struct rlimit _;                                                                 \
    _.rlim_cur = (value);                                                            \
    _.rlim_max = value + ext;                                                        \
    if ( setrlimit( type , & _ ) != 0 ) {                                            \
        fprintf( stdout , "Setrlimit error(%s): %s\n" , #type , strerror(errno) );   \
        exit( -1 );                                                                  \
    }                                                                                \
}while(0)

void genrate_running_command(){
    sprintf( running_arguments , "./%s.bin" , running_sourcefile );
}

void genrate_checker_command(){
    sprintf( checker_arguments , "./%s.bin %s %s %s 1>/dev/null 2>&1" , checker_sourcefile , input_sourcefile , output_sourcefile , answer_sourcefile );
}

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
    if( argc != 10 ) errExit( "Arguments number should be 9" );
    timelimit = atoll( argv[1] );
    memorylimit = atoll( argv[2] );
    outputlimit = atoll( argv[3] );
    stacklimit = atoll( argv[4] );
    input_sourcefile = argv[5];
    output_sourcefile = argv[6];
    answer_sourcefile = argv[7];
    running_sourcefile = argv[8];
    checker_sourcefile = argv[9];
    genrate_running_command();
    genrate_checker_command();
    pid = fork();
    if( pid > 0 ){
        struct rusage result;
        int status;
        pthread_t watch_thread;
        if(pthread_create( & watch_thread , NULL , ( void * )wait_to_kill_childprocess , NULL ))
            errExit( "Can not create watch pthread" );
        wait4( pid , & status , 0 , & result );
        int status_code = get_status_code( WEXITSTATUS(status) );
        if( status_code == -1 ) errExit( "Unknown Error" );
        if( status_code == 127 ) errExit( "Can not run target program" );
        long long timecost = ( long long )result.ru_utime.tv_sec * 1000000ll + ( long long )result.ru_utime.tv_usec;
        if( status_code == SIGXCPU || timecost > 1ll * timelimit * 1000 || Exceeded_wall_clock_time ) goodExit( "Time Limit Exceeded" , timelimit , result.ru_maxrss  );
        if( status_code == SIGXFSZ ) goodExit( "Output Limit Exceeded" , timecost / 1000 , result.ru_maxrss );
        if( result.ru_maxrss > memorylimit ) goodExit( "Memory Limit Exceeded" , timecost / 1000 , result.ru_maxrss );
        if( status_code != 0 ) goodExit( "Runtime Error" , timecost / 1000 , result.ru_maxrss );
        int checker_statuscode = system( checker_arguments );
        if( checker_statuscode == 0 ) goodExit( "Accepted" , timecost / 1000 , result.ru_maxrss ); 
        else if( checker_statuscode > 256 ) errExit( "Checker error" );
        goodExit( "Wrong Answer" , timecost / 1000 , result.ru_maxrss ); 
    }else if( pid == 0 ){
        set_limit( RLIMIT_CPU , ( timelimit + 999 ) / 1000 , 1 ); // set cpu_time limit
        set_limit( RLIMIT_AS , memorylimit , ( 1 << 10 ) ); // set memory limit
        set_limit( RLIMIT_FSIZE , outputlimit , 0 ); // set output limit
        set_limit( RLIMIT_STACK , stacklimit , 0 ); // set stack limit
        if( freopen( input_sourcefile , "r" , stdin ) == NULL ) errExit( "Can not redirect stdin" );
        if( freopen( output_sourcefile , "w" , stdout ) == NULL ) errExit( "Can not redirect stdout" );
        execl( "/bin/sh", "sh", "-c",  running_arguments , (char *) 0);
    }else
        errExit( "Can not fork the child process" );
    return 0;
}