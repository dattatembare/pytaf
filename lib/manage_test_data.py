import os

from lib.commandline_args import cargs
from lib.utils import load_data

THIS_DIR_PATH = os.path.dirname(os.path.abspath(__file__))
TEST_DATA_DIR = '../test_data'


def get_test_data(test_data_file: str, env: str = None) -> dict:
    """
    Pull test data json file and convert to dictionary
    :param test_data_file: test data file name
    :param env: env
    :return: test data dictionary
    """
    test_data_file = f'{THIS_DIR_PATH}/{TEST_DATA_DIR}/{test_data_file}'
    return load_data(test_data_file).get(env, {}) if env else load_data(test_data_file)


def test_data(**dec_kwargs):
    def decorator(func):
        def wrapper(*args, **kwargs):
            kwargs = {**kwargs, **env_test_data(dec_kwargs.get("file_name"))}
            exec_func = func(*args, **kwargs)
            return exec_func

        return wrapper

    return decorator


def env_test_data(test_data_file) -> dict:
    """
    Make ENV specific test data available at top level.
    :param test_data_file: test data file path
    :return: test data dict
    """
    _cargs = cargs()
    _env = _cargs.environment
    _ext_td = _cargs.test_data
    _td_file = _ext_td if _ext_td else test_data_file
    _test_data = get_test_data(_td_file)
    assert '.json' in _td_file, 'Invalid test_data file name, provide valid json file'
    _test_data = get_test_data(_td_file)
    if not _test_data:
        # Full qualified path for external test data file
        _test_data = load_data(_td_file)

    _env_data = {**_test_data.get(_env, {}), **_test_data.get(_env.upper(), {})}

    for env_ele, env_val in _env_data.items():
        if type(env_val) == dict:
            _test_data[env_ele] = {**_test_data.get(env_ele, {}), **env_val}
            _env_data[env_ele] = {**_test_data.get(env_ele, {}), **env_val}
        else:
            _test_data[env_ele] = env_val
            _env_data[env_ele] = env_val

    return _test_data


def get_expected_response(expected_res: str, env: str = None, **test_data) -> dict:
    """
    Get expected response
    :param expected_res: key name
    :param env: env
    :param test_data: test data kwargs
    :return: expected response dict
    """
    assert test_data, 'test_data is missing, pass valid test_data'
    common_for_all = test_data.get('expected_response', {}).get(expected_res, {})
    env_res = test_data.get(env, {}).get('expected_response', {}).get(expected_res, {})
    if type(common_for_all) == dict and type(env_res) == dict:
        return {**common_for_all, **env_res}
    elif env_res:
        return env_res
    elif common_for_all:
        return common_for_all
