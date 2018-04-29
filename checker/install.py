from progressive.bar import Bar
import os
import sys

compile_command = ' g++ -o {sourcefile}.bin  \
                    ../testlib/checkers/{sourcefile}.{extension} \
                    -O2 -std=gnu++17         \
                    -I ../testlib'

list_dir = list( filter(  lambda x : os.path.splitext( x )[1] == '.cpp' , os.listdir( '../testlib/checkers' ) ) )
bar = Bar( max_value = len( list_dir ) )
bar.title = 'Install checker'
bar.cursor.clear_lines(2)
bar.cursor.save()
bar.draw(value=0)

for i , _ in enumerate(list_dir):
    sourcefile , extension = os.path.splitext( _ )
    running_arguments = compile_command.format(
        sourcefile = sourcefile,
        extension = extension[1:]
    )
    os.system( running_arguments )
    bar.cursor.restore()
    bar.draw( value = i + 1 )
