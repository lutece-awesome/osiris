from tqdm import tqdm
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

testlib_compile_command = 'docker run --rm -v ' + BASE_DIR + ':/home -w /home osiris-gcc:7.3.0 \
                           g++ -o checker/{sourcefile}.bin testlib/checkers/{sourcefile}.{extension} \
                           -O2 -std=gnu++17 -I testlib'

list_dir = list(filter(lambda x: os.path.splitext(
    x)[1] == '.cpp', os.listdir('testlib/checkers')))

print('Building checkers...')
for file in tqdm(list_dir):
    sourcefile, extension = os.path.splitext(file)
    running_arguments = testlib_compile_command.format(
        sourcefile=sourcefile,
        extension=extension[1:]
    )
    os.system(running_arguments)

core_compile_command = 'docker run --rm -v ' + BASE_DIR + ':/home -w /home osiris-gcc:7.3.0 \
                        gcc -o core/core.bin core/core.c -O2 -lpthread'

print('Building core...')
os.system(core_compile_command)
