

# The list of SUPPORT_LANGUAGE
SUPPORT_LANGUAGE = {
    'GNU G++17':{
        'docker_repo' : 'gcc',
        'docker_repo_tag' : '7.3.0',
        'extension' : 'cpp',
        'compile_command' : 'timeout -s KILL {compile_timeout} g++ -w -O2 -DONLINE_JUDGE --std=gnu++17 \
                            {source_file}.{extension} -lm -o {source_file}.bin'
    },

    'CLANG++17':{
        'extension' : 'cpp',
    },

    'GNU GCC 7.3':{
        'extension' : 'c',
    },

    'Python 3.6.5':{
        'extension' : 'py',        
        'compile_command' : 'mv {source_file}.{extension} {source_file}.bin'
    },

    'Python 2.7.12':{
        'extension' : 'py',        
    },

    'Java 1.9.0':{
        'extension' : 'java',        
    },
}
