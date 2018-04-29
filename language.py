# The list of SUPPORT_LANGUAGE
SUPPORT_LANGUAGE = {
    'GNU G++17':{
        'image' : 'osiris-gcc:7.3.0',
        'extension' : 'cpp',
        'compile_command' : 'g++ -w -O2 -DONLINE_JUDGE -fmax-errors=15 --std=gnu++17 \
                            {sourcefile}.{extension} -lm -o {sourcefile}.bin',
        'running_command' : './{sourcefile}.bin'
    },

    'Clang 6.0.0':{
        'extension' : 'cpp',
    },

    'GNU GCC 7.3':{
        'extension' : 'c',

        'compile_command' : 'gcc -w -O2 -DONLINE_JUDGE -fmax-errors=15 --std=c11 \
                            {sourcefile}.{extension} -lm -o {sourcefile}.bin'
    },

    'Python 3.6.5':{
        'extension' : 'py',        
        'compile_command' : 'mv {sourcefile}.{extension} {sourcefile}.bin'
    },

    'Python 2.7.12':{
        'extension' : 'py',        
    },

    'Java 1.9.0':{
        'extension' : 'java',        
    },
}


running_shell_arguments = '                                                                                                                                                 \
    #!/bin/bash                                                                                                                                                             \
    time_limit={time_limit}                                                                                                                                                 \
    memory_limit={memory_limit}                                                                                                                                             \
    output_limit={output_limit}                                                                                                                                             \
    stack_limit={stack_limit}                                                                                                                                               \
    checker={checker}                                                                                                                                                       \
    running_core={core}                                                                                                                                                     \
    sourcefile={sourcefile}                                                                                                                                                 \
    data_dir={data_dir}                                                                                                                                                     \
    case_number={case_number}                                                                                                                                               \
    for(( i = 1 ; i <= case_number ; ++ i))                                                                                                                                 \
    '+ r' do                                                                                                                                                                    \
        result=$(${running_core} ${time_limit} ${memory_limit} ${output_limit} ${stack_limit}  ${data_dir}/${i}.in user.out ${data_dir}/${i}.out ${sourcefile} ${checker})  \
        status_code=$?                                                                                                                                                      \
        printf \'{\"case\":\"%s\",\"info\":%s}\n\' \"$i\" \"$result\"                                                                                                       \
        if [ $status_code -ne 0 ]; then                                                                                                                                     \
            exit -1                                                                                                                                                         \
        fi                                                                                                                                                                  \
        echo "$result" | grep -q "Accepted"                                                                                                                                 \
        if [ $? -ne 0 ]; then                                                                                                                                               \
            exit 0                                                                                                                                                          \
        fi                                                                                                                                                                  \
    done                                                                                                                                                                    \
'                                           


def get_extension( lang ):
    return SUPPORT_LANGUAGE[lang]['extension']

def get_compile_command( lang ):
    return SUPPORT_LANGUAGE[lang]['compile_command']

def get_image( lang ):
    return SUPPORT_LANGUAGE[lang]['image']

def get_running_command( lang ):
    return SUPPORT_LANGUAGE[lang]['running_command']