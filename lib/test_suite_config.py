"""
Test Suite Configuration structure: this file name will be used as commandline argument to run the test suite.
This suite contains parameters like - ssoguid, run_tests and more
    ## run_tests: defines test to be run as part of the suite
    {
        "module": "test.company_tasks_svc.test_company_tasks_svc",  # Mandatory if new {} added in config file
        "classes": [                                                # Optional element, if not preset or empty,
                {                                                       then all classes methods will be executed
              "test_class": "HealthCheck",              # test_class with/without list of methods
              "test_methods": [                                     # If test_methods not provided then run all methods
                "test_health_check_success"
              ]
            }
        ]
    }

Python Suite configuration structure: this config file contains information requited to run python test suites.
    Ex. sanity_suite - This sub-suite has parameters like baseurl and endpoints list

"""
import glob
import os
from functools import lru_cache
from types import MappingProxyType

from lib.commandline_args import get_args_dict
from lib.utils import load_data, get_resource_config

DATA_DIR = '../test_data/default'
SUITE_DIR = '../suite'
CURRENT_DIR_PATH = os.path.dirname(os.path.abspath(__file__))


@lru_cache()
def load_suite_config(**command_args) -> MappingProxyType:
    """
    return suite configs as a Tuple
    :return: TWare object for config dict
    """
    args_dict = command_args if command_args else get_args_dict()
    environment = args_dict.get('environment')
    overall_cfg_dict = {**args_dict, **get_resource_config(), 'environment': environment}

    # Gather all tests for test suits (entered from commandline/TAF input)
    # Tests configuration is in <suite_name>.json Ex. sanity_suite.json
    run_suites = _parse_selected_suites(args_dict)
    run_tests = []
    for run_suite in run_suites:
        _suite_name = run_suite if '.json' in run_suite else f'{run_suite}.json'
        run_suite_env_cfg_pn = f"{CURRENT_DIR_PATH}/{SUITE_DIR}/{_suite_name}"
        run_suite_env_cfg_dict = load_data(run_suite_env_cfg_pn, print_error=True)
        run_tests.extend(run_suite_env_cfg_dict.get('run_tests', []))

    overall_cfg_dict["run_tests"] = run_tests

    # Pull all .json files recursively from test_data/default
    suite_default_test_data_files = [file for file in
                                     glob.iglob(f'{CURRENT_DIR_PATH}/{DATA_DIR}/**/*.json', recursive=True)]

    # Get python suites from resource_config.json and pull its default data from test_data/default
    for suite, data in overall_cfg_dict['suites'].items():
        suite_env_cfg_file = f"{suite}_{environment}.json"
        suite_default_test_data_file = [suite_file for suite_file in suite_default_test_data_files
                                        if suite_env_cfg_file in suite_file]
        suite_env_cfg_dict = load_data(suite_default_test_data_file[0]) if suite_default_test_data_file else {}
        overall_cfg_dict['suites'][suite] = {**data, **suite_env_cfg_dict}

    # MappingProxyType - Read-only proxy of a mapping. Used to make dictionary immutable.
    return MappingProxyType(overall_cfg_dict)


def _parse_selected_suites(args_dict) -> list:
    """
    return suite list
    :param args_dict: all commandline arguments
    :return: list of suite names
    """
    suites = args_dict.get('suite')
    return str(suites).split(',') if suites else []
