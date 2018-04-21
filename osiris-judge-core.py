import argparse
from settings import SUPPORT_LANGUAGE

parser = argparse.ArgumentParser(description='Osiris Judge Core.')

parser.add_argument('-l', '--language', required = True, type = str, dest = 'language_token',
                    choices = SUPPORT_LANGUAGE,
                    help= 'The language of code' )


args = parser.parse_args()
