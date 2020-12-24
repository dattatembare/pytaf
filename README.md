# PyTAF - Python Testing Automation Framework

Python Testing Automation Framework for service endpoint testing automation

# PyTAF project Structure:

    pytaf
    ├───config                                              <-- Configuration files
    │   ├───company_task
    |   |   └───company_task_resource_config.json
    │   ├───auth.json                                       <-- Basic authentication key generated using update_auth.py
    │   ├───logger_config.json                              <-- Logger config
    │   ├───resource_config.json                            <-- All end point entries
    ├───lib
    │   ├───utils.py
    ├───suite                                               <-- Configuration used to run the multiple tests
    │   ├───sanity_suite.json
    ├───test                                                <-- main test suite
    │   ├───company_tasks_svc                               <-- endpoint service sub-suite
    │   │   └───<tests>
    ├───test_data                                           <-- Test data (Overrides default test data)
    │   ├───default                                         <-- Suite and endpoint specific default test data
    │   │   ├───company_task
    |   │   │   └───company_tasks_svc_dev.json
    ├───utilities                                           <-- Utilities which can be called independently from command-line
    │   └───<add utilities>
    └───zlogs                                               <-- logs
    │   └───pytaf.log
    ├───requirements.txt                                    <-- file contains all required external modules
    ├───test_launcher.py                                    <-- Single point to call one or multiple tests
    ├───update_auth.py                                      <-- First thing to do before executing any test
    └───README.md                                           <-- This file

# Easy 3 steps method to add automation tests to your endpoint -
1. Add/update resource config with endpoint details like base url, endpoint method and path
2. Add test data - it will contain request params, path variables and request body (for POST, PUT, PATCH)
3. Write tests - Write unittest, access test data using @test_data decorator.
To run the tests use below steps. 

# Before running the tests -
Update config/auth.json for basic authentication, If authentication not required in your work env then skip this step and make code changes to skip this check.

This authentication is appended in headers of each endpoint request. Authentication details in 'auth.json' is required to run the service endpoint tests on all environments. 
If this file is not available in expected config directory then test execution will be abruptly stopped and throw the error about unavailability of file.

Run below command from commandline/terminal to update authorization config file.

`client=pytaf>update_auth.py`

Enter username/password and you are all set.

# Run commands:

1. Know about command-line arguments:
    
    `pytaf>test_launcher.py -h`
    
2. Find all tests in Python test suite: Command will result all the tests from Python suite (all tests under "test" directory and sub-directories).
The output format for test names will be `<module_path>.<class_name>.<test_method_name>` Ex. `test.company_tasks_svc.test_company_tasks_svc.HealthCheck`

    `pytaf>test_launcher.py -ts`

3. Find tests which contains "task": Command will result all the tests from Python suite which path contains text "task"

    `pytaf>test_launcher.py -ts task`

4. Run single test: command will run single test from Python test suite

    `pytaf>test_launcher.py -e dev -a test.company_tasks_svc.test_company_tasks_svc.HealthCheck.test_health_check_success`

5. Run two or multiple tests: Add two or more test with comma(,) separated
    
    `pytaf>test_launcher.py -e dev -a test.company_tasks_svc.test_company_tasks_svc.HealthCheck.test_health_check_success,test.enterprise_company_svc.test_liveness.TestLiveness.test_liveness_success`

6. Run single Suite:

    `pytaf>test_launcher.py -e dev -s sanity_suite`


*New Features:*

1. Endpoint suits globally available, it reduces endpoint call function layer.
2. Add http methods in resource_config.json
3. Logging for verbosity.
4. Top level and env specific test data is pre-cooked to use directly in tests.
5. Commandline arguments are globally available.
6. resource_config reading multiple resource files from hierarchy
7. suite endpoint default test data is now under test_data/default
