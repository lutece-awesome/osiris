import argparse

parser = argparse.ArgumentParser( description = 'Storyline File System.' )

parser.add_argument( '--pull', required = True, type = int, dest = 'problem_id',
                    help = 'The problem_id of pull.' )


args = parser.parse_args()

