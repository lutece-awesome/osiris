# The list of SUPPORT_LANGUAGE
SUPPORT_LANGUAGE = {
    'GNU G++17':{
        'image' : 'osiris-gcc:7.3.0',
        'running_extension' : '.bin',
        'extension' : 'cpp',
        'compile' : True,
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
        'image' : 'osiris-python:3.6.5-stretch',
        'running_extension' : '.py',
        'extension' : 'py',
        'compile' : False,
        'running_command' : 'python3 {sourcefile}.py'
    },

    'Python 2.7.12':{
        'extension' : 'py',        
    },

    'Java 1.9.0':{
        'extension' : 'java',        
    },
}


def get_extension( lang ):
    return SUPPORT_LANGUAGE[lang]['extension']

def get_compile_command( lang ):
    return SUPPORT_LANGUAGE[lang]['compile_command']

def get_image( lang ):
    return SUPPORT_LANGUAGE[lang]['image']

def get_running_command( lang ):
    return SUPPORT_LANGUAGE[lang]['running_command']

def get_running_extension( lang ):
    return SUPPORT_LANGUAGE[lang]['running_extension']

def need_compile_ornot( lang ):
    return SUPPORT_LANGUAGE[lang]['compile']