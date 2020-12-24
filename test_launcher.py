import glob
import importlib
import sys
import unittest
from os.path import dirname, normpath
from unittest import TextTestRunner

from lib.test_suite_config import load_suite_config, get_args_dict
from lib.utils import trace

BASE_PATH = dirname(__file__)


def find_test_classes(suite_config) -> unittest.TestSuite:
    """
    Finds the candidate test classes within the given path
    :param suite_config: the test suite configuration
    :return: the list of matching test case classes
    """

    # Retrieve the selected suite (input from commandline or TAF), if given.
    # None means all scanned test classes will be run.
    run_modules = []
    run_classes = {}
    for module_tuple in suite_config.get('run_tests'):
        try:
            run_modules.append(module_tuple.get('module'))
        except AttributeError:
            raise AttributeError("Add mandatory element 'module' or remove empty '{}' configuration block")
        run_classes[module_tuple.get('module')] = module_tuple.get('classes', '')

    # find and import test modules
    find_and_import_modules(run_modules)

    # Add all run_tests configured in the suite configuration file Ex. sanity_suite.json
    suite = unittest.TestSuite()
    for _class in unittest.TestCase.__subclasses__():
        if _class.__module__.startswith('test.'):
            class_tuples = run_classes.get(_class.__module__, [])
            # When classes element is empty or not present add all tests in the module
            if not class_tuples:
                suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(_class))
            # Add listed tests for configured classes
            add_configured_test_methods(_class, class_tuples, suite)

    return suite


def add_configured_test_methods(_class, class_tuples, suite) -> None:
    """
    Add configured test methods to TestSuite
    :param _class:
    :param class_tuples:
    :param suite:
    :return: None
    """
    for class_tuple in class_tuples:
        if _class.__name__ == class_tuple.get('test_class'):
            _test_methods = class_tuple.get('test_methods', [])
            # When classes element is present but methods list not provided then add all test methods from that class
            if not _test_methods:
                suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(_class))
            # Add listed methods
            for test_method in _test_methods:
                suite.addTest(unittest.defaultTestLoader.loadTestsFromName(
                    f"{_class.__module__}.{_class.__name__}.{test_method}"))


def find_and_import_modules(run_modules) -> None:
    """
    Find expected test modules to run and import using importlib
    :param run_modules:
    :return:
    """
    tests_directory_path = normpath(f'{BASE_PATH}/test')
    for filename in glob.iglob(f'{tests_directory_path}/**/*.py', recursive=True):
        filename = normpath(filename).replace('.py', '').replace('\\', '.').replace("/", '.')
        module_name = filename[filename.find('.test.') + 1:]
        if not run_modules or module_name in run_modules:
            importlib.import_module(module_name)


@trace(text='Searching tests')
def tests_list(search_text) -> list:
    """
    return searched list for input text, if search_text is * then return all tests from python "test" suite
    :param search_text:
    :return: tests list
    """
    tests = []
    find_and_import_modules([])
    for _class in unittest.TestCase.__subclasses__():
        if _class.__module__.startswith('test.'):
            for test_method in unittest.defaultTestLoader.loadTestsFromTestCase(_class):
                test_method = test_method.__str__()[:test_method.__str__().find('(')]
                test_method = f"{_class.__module__}.{_class.__name__}.{test_method.strip()}"
                if '*' == search_text or search_text.lower() in test_method.lower():
                    print(test_method)
                    tests.append(test_method)
    return tests


def add_tests_to_suite(add_tests: list) -> unittest.TestSuite:
    """
    Add test/s to TesSuite
    :param add_tests: list of full test paths
    :return: TestSuite
    """
    suite = unittest.TestSuite()
    for add_test in add_tests:
        suite.addTest(unittest.defaultTestLoader.loadTestsFromName(add_test))
    return suite


@trace(text="Running Tests")
def test_runner(suite):
    """
    Test Runner
    :param suite:
    :return:
    """
    # verbosity=2 unittest will print the result of each test run.
    TextTestRunner(stream=sys.stdout, verbosity=2).run(suite)


def run_test_suite() -> None:
    """
    Run whole test suite
    :return: None
    """
    # note that command line arguments are parsed within test_suite_config module
    args_dict = get_args_dict()
    search_text = args_dict.get('test_search')
    if search_text:
        tests = tests_list(search_text)
        exit(0)

    suite_config = load_suite_config()

    add_tests = args_dict.get('add_tests')
    if add_tests:
        # run tests passed as a commandline argument
        suite = add_tests_to_suite(add_tests.split(','))
    else:
        # run tests configured in config file/s Ex. sanity_suite.json
        suite = find_test_classes(suite_config)

    print('\n')
    test_runner(suite)


"""
How to run unit_test_launcher: 
client=pytaf>python -m test_launcher -e <environment> -s <suite>
-e optional/default value is dev, -s optional/default value is all suits
"""
if __name__ == '__main__':
    run_test_suite()
