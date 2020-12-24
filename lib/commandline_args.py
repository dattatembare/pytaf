from argparse import ArgumentParser
from functools import lru_cache

from lib.tupleware import tupleware
from lib.utils import format_env


@lru_cache()
def get_args_dict() -> dict:
    parser = ArgumentParser()
    parser.add_argument('-e', '--environment', help='Environment (default=dev)', default='dev')
    parser.add_argument('-s', '--suite', help='Single or multiple comma separated Test Suites')
    parser.add_argument('-a', '--add_tests', help='Single or multiple comma separated list of tests')
    parser.add_argument('-ts', '--test_search', nargs='?', const='*',
                        help='Tests Search using text entry or default "*" which returns all tests')
    parser.add_argument('-td', '--test_data', help='Test data file name or full qualified file path')
    parser.add_argument('-l', '--log_level', help='Log level, default is INFO', default='INFO')

    return format_env(parser.parse_args().__dict__)


def cargs():
    return tupleware(get_args_dict())
