import json
from functools import lru_cache

from lib import send_request, HttpResponse
from lib.common_namedtuples import EndPoint
from lib.test_suite_config import load_suite_config
from lib.tupleware import tupleware
from lib.utils import get_auth, get_resource_config


def call_endpoint(endpoint_config: 'TWare', method: str = None, command_args: dict = None, input_args: dict = None,
                  **kwargs) -> HttpResponse:
    """
    Prepare endpoint and call the endpoint with appropriate url and headers
    :param endpoint_config: endpoint object contains suite name, endpoint name key to prepare complete endpoint
    :param method: http method, use if provided
    :param command_args: commandline arguments for non test utilities
    :param input_args: input arguments to prepare endpoint url
    :param kwargs: other keyword arguments
    :return: EndPoint
    """
    configs = load_suite_config(**command_args) if command_args else load_suite_config()
    _env = configs.get('environment')
    _suite = configs.get('suites').get(endpoint_config.suite)

    # Suite level data (considered as default)
    _base_url, _suite_args, _suite_params, _suite_headers = get_suite_level_data(_suite, _env, endpoint_config.endpoint)
    # Test data set in internal/test_data directory (it will override suite level default data)
    _td_args, _td_params, _td_headers, _td_data, _td_json = get_internal_test_data(_env, **kwargs)

    # Prepare endpoint, headers, data, files and json
    _input_args = input_args if input_args else {}
    _endpoint_args = {**_suite_args, **_td_args, **_input_args}
    _endpoint_args = {**_endpoint_args, **command_args} if command_args else _endpoint_args

    # Parameters for GET request
    _params = {**_suite_params, **_td_params}

    _endpoint_path = _suite.get('endpoints').get(endpoint_config.endpoint).get('path').format(**_endpoint_args)
    _uri = f"{_base_url}{_endpoint_path}"

    # Add additional headers if provided by calling method
    _headers = {**_suite_headers, **_td_headers, **kwargs.get('add_headers', {}), **get_auth()}

    _method = method if method else _suite.get('endpoints').get(endpoint_config.endpoint).get('method')
    endpoint_obj = EndPoint(uri=_uri, method=_method.lower(), env=_env, headers=_headers, params=_params,
                            data=_td_data, json=_td_json)

    return send_request(endpoint_obj)


def get_suite_level_data(suite: dict, env: str, endpoint_key: str) -> tuple:
    """
    This data considered as default data if setup in suite level file
    :param suite: suite name
    :param env: env
    :param endpoint_key: endpoint key
    :return: tuple of url, args and headers
    """
    _base_url = suite.get(f'{env}_baseurl', suite.get('baseurl').format(environment=env))
    _suite_args = suite.get(endpoint_key, {}).get('args', {})
    _suite_params = suite.get(endpoint_key, {}).get('params', {})
    _suite_headers = suite.get(endpoint_key, {}).get('headers', {})

    return _base_url, _suite_args, _suite_params, _suite_headers


def get_internal_test_data(env: str, **test_data) -> tuple:
    """
    This data is coming from test_data directory json file. It will override the suite level data.
    :param env: env
    :param test_data: test data
    :return: tuple of args, headers, data and json
    """
    env_data = test_data.get(env, {})
    td_args = {**test_data.get('args', {}), **env_data.get('args', {})}
    td_params = {**test_data.get('params', {}), **env_data.get('params', {})}
    td_headers = {**test_data.get('headers', {}), **env_data.get('headers', {})}

    # If non dictionary data then convert to json string
    td_data = {}
    if type(test_data.get('data')) == dict:
        td_data = {**test_data.get('data'), **env_data.get('data')} if type(
            env_data.get('data')) == dict else test_data.get('data')
    elif env_data.get('data'):
        td_data = json.dumps(env_data.get('data'))
    elif test_data.get('data'):
        td_data = json.dumps(test_data.get('data'))

    if type(test_data.get('json')) == dict:
        td_json = {**test_data.get('json'), **env_data.get('json')} if type(
            env_data.get('json')) == dict else test_data.get('json')
    else:
        td_json = env_data.get('json') if env_data.get('json') else test_data.get('json', {})

    return td_args, td_params, td_headers, td_data, td_json


@lru_cache()
def endpoint_suites() -> 'TWare':
    """
    Formatted Endpoints data to access as endpoints.<endpoint suite>.<end point>
    :return:TWare object
    """
    _suites = {}
    for k, v in get_resource_config()['suites'].items():
        _suite = {'suite': k}
        base_url = v['baseurl']
        del v['baseurl']
        for k1, v1 in v.get('endpoints', {}).items():
            v1['suite'] = k
            v1['endpoint'] = k1
            v1['path'] = f'{base_url}{v1["path"]}'
            v1['method'] = v1.get('method', 'GET')
            _suite[k1] = v1
        _suites[k] = _suite
    return tupleware(_suites)


# Access formatted Endpoints data as endpoints.<endpoint suite>.<end point>
endpoints = endpoint_suites()
