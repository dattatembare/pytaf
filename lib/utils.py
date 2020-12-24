import getpass
import json
import os
from base64 import b64encode
from typing import Generator

THIS_DIR_PATH = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = '../config'
SUITE_DIR = '../suite'
AUTH_CONFIG = 'auth.json'
RESOURCE_CONFIG = 'resource_config.json'
LOGGER_CONFIG = 'logger_config.json'
RESOURCE_CONFIGS_DIR = f"{THIS_DIR_PATH}/{CONFIG_DIR}"


def headline(text, border="*", width=100) -> None:
    """
    Print statements with border
    :param text: text to print
    :param border: border character
    :param width: leading and trailing width
    :return: None
    """
    print(f" {text} ".center(width, border))


def trace(**deckwargs):
    def decorator(func):
        def wrapper(*args, **kwargs):
            text = deckwargs.get("text", func.__name__)
            headline(f"START {text}")
            exec_func = func(*args, **kwargs)
            headline(f"END {text}")
            return exec_func

        return wrapper

    return decorator


def slice_generator(in_gen: Generator, slice_for: int) -> list:
    """
    slice generator
    :param in_gen: generator
    :param slice_for: slice first counts
    :return: list
    """
    sliced_list = []
    for i, item in enumerate(in_gen):
        sliced_list.append(item)
        if i == slice_for - 1:
            break
    return sliced_list


def load_data(file_path: str, print_error=False) -> dict:
    """
    Load test data from json config files to python dictionary
    :param file_path: file path to read
    :param print_error: boolean, if True print error
    :return: config dict
    """
    try:
        with open(file_path, 'rb') as f:
            return json.loads(f.read())
    except (OSError, FileNotFoundError):
        if print_error:
            if AUTH_CONFIG in file_path:
                print(f"\nAuthentication config file 'config/auth.json' is not available in expected config directory, "
                      f"to create it follow the instructions in README.md")
                exit(1)
            else:
                print(f"Warning: File name is incorrect or config file {file_path} not exist")
        return {}


def get_auth() -> dict:
    """
    Get basic authentication key
    :return: authentication key
    """
    return load_data(f'{THIS_DIR_PATH}/{CONFIG_DIR}/{AUTH_CONFIG}', True)


def get_basic_auth_key() -> str:
    """
    Generate basic authentication key.
    :return: authentication key
    """
    user = getpass.getpass(prompt='Username:')
    password = getpass.getpass(prompt='Password:')
    user_pass = b64encode(f"{user}:{password}".encode()).decode("ascii")
    return f'Basic {user_pass}'


def get_resource_config() -> dict:
    """
    Pull resource_config data and return as dictionary
    :return: resource config
    """
    _suites = {}
    for suite in load_data(f"{RESOURCE_CONFIGS_DIR}/{RESOURCE_CONFIG}").get('suites'):
        _suites.update(load_data(f'{RESOURCE_CONFIGS_DIR}/{suite}'))

    return {'suites': _suites}


def get_logger_config() -> dict:
    """
    Pull logger configs and return as dictionary
    :return: resource config
    """
    return load_data(f"{THIS_DIR_PATH}/{CONFIG_DIR}/{LOGGER_CONFIG}")


def format_response(response, message: str = None) -> str:
    """
    return formatted response message
    :param response: endpoint call response object
    :param message: customized message
    :return: message str
    """
    return f"{message if message else 'Error Message:'}\n" \
           f"Status Code: {response.status}\n" \
           f"URL: {response.url}\n" \
           f"sec-id: {response.headers.get('sec-id', '')}\n" \
           f"x-txid: {response.transaction-id}\n" \
           f"Data: {response.data}"


def format_env(args_dict: dict) -> dict:
    """
    Change environment argument value to lowercase, change dev+1 -> dev1, DEV->dev0
    :param args_dict: dictionary of commandline arguments
    :return: dictionary with formatted env
    """
    if args_dict.get('environment'):
        _env = args_dict.get('environment').replace('+', '').lower()
        _env = f'{_env}0' if _env == 'n' else _env
        args_dict['environment'] = _env
    return args_dict