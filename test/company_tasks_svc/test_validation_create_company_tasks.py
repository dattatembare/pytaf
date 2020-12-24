import copy
import unittest

from lib.manage_test_data import test_data, get_expected_response
from lib.utils import format_response
from test.company_tasks_svc.endpoint_call_helpers import delete_all_company_tasks, create_company_tasks


class TestValidationCreateCompanyTasksSvc(unittest.TestCase):

    @test_data(file_name="company_tasks_svc/validation_create_company_tasks.json")
    def test_company_tasks_error_when_companyid_not_match(self, **file_test_data):
        """
        Scenario:
            When the createCompanyTasks endpoint is called and the companyid in URL does not match companyid in one or more
            proto-tasks in endpoint inputs, confirm:
                Response contains Status code 400
                error is reported
                no tasks are created
        Test plan steps:
            1. Set test data - companyid in URL does not match companyid in one or more proto-tasks
            2. Call Call createCompanyTasks endpoint
            3. verify response
        """
        # Set test data
        file_test_data['json'][0]['companyid'] = 'SOMEOTHEREcompanyid'

        # Call create task endpoint and verify
        self._call_endpoint_and_verify_response('invalid_companyid_response', **file_test_data)

    @test_data(file_name="company_tasks_svc/validation_create_company_tasks.json")
    def test_company_tasks_error_when_companyid_missing(self, **file_test_data):
        """
        Scenario:
            When the createCompanyTasks endpoint is called and One or more proto-tasks in endpoint inputs is missing
            required field [companyid], confirm:
                Response contains Status code 400
                error is reported in data
                no tasks are created
        Test plan steps:
            1. Set test data - delete companyid in one or more proto-tasks
            2. Call Call createCompanyTasks endpoint
            3. verify response
        """
        # Set test data
        file_test_data['json'][0].pop('companyid')

        # Call create task endpoint and verify
        self._call_endpoint_and_verify_response('invalid_companyid_response', **file_test_data)

    @test_data(file_name="company_tasks_svc/validation_create_company_tasks.json")
    def test_company_tasks_error_when_missing_required_field(self, **file_test_data):
        """
        Scenario:
            When the createCompanyTasks endpoint is called and One or more proto-tasks in endpoint inputs is missing
            required field(s) [category, type, or assignees], confirm:
                Response contains Status code 400
                error is reported in data
                no tasks are created
        Test plan steps:
            1. Set test data - delete required field(s) [category, type, or assignees] in one or more proto-tasks
            2. Call Call createCompanyTasks endpoint
            3. verify response
        """
        # Set test data for missing category
        _test_data = copy.deepcopy(file_test_data)
        _test_data['json'][0].pop('category')

        # Call create task endpoint and verify
        self._call_endpoint_and_verify_response('missing_required_field_response', **_test_data)

        # Set test data for missing type
        _test_data = copy.deepcopy(file_test_data)
        _test_data['json'][0].pop('type')

        # Call create task endpoint and verify
        self._call_endpoint_and_verify_response('missing_required_field_response', **_test_data)

        # Set test data for missing assignees
        _test_data = copy.deepcopy(file_test_data)
        _test_data['json'][0].pop('assignees')

        # Call create task endpoint and verify
        self._call_endpoint_and_verify_response('missing_required_field_response', **_test_data)

    @test_data(file_name="company_tasks_svc/validation_create_company_tasks.json")
    def test_company_tasks_error_when_empty_assignees(self, **file_test_data):
        """
        Scenario:
            When the createCompanyTasks endpoint is called and One or more proto-tasks in endpoint inputs with one or
            more empty assignees, confirm:
                Response contains Status code 400
                error is reported in data
                no tasks are created
        Test plan steps:
            1. Set test data - set empty assignee in one or more proto-tasks
            2. Call Call createCompanyTasks endpoint
            3. verify response
        """
        # Set test data
        assignees = file_test_data['json'][0]['assignees']
        assignees.append({})
        file_test_data['json'][0]['assignees'] = assignees

        # Call create task endpoint and verify
        self._call_endpoint_and_verify_response('empty_assignees_response', **file_test_data)

    @test_data(file_name="company_tasks_svc/validation_create_company_tasks.json")
    def test_company_tasks_error_when_id_in_input(self, **file_test_data):
        """
        Scenario:
            When the createCompanyTasks endpoint is called and One or more proto-tasks in endpoint inputs with id field,
            confirm:
                Response contains Status code 400
                error is reported in data
                no tasks are created
        Test plan steps:
            1. Set test data - Add id in one or more create proto-tasks
            2. Call Call createCompanyTasks endpoint
            3. verify response
        """
        # Set test data
        file_test_data['json'][0]['id'] = 'when-id-is-present-in-input'

        # Call create task endpoint and verify
        self._call_endpoint_and_verify_response('id_present_in_input', **file_test_data)

    @test_data(file_name="company_tasks_svc/validation_create_company_tasks.json")
    def test_company_tasks_error_when_invalid_status(self, **file_test_data):
        """
        Scenario:
            When the createCompanyTasks endpoint is called and One or more proto-tasks in endpoint inputs with a status
            not in the list: [CREATED, COMPLETED, IN_PROGRESS] , confirm:
                Response contains Status code 400
                error is reported in data
                no tasks are created
        Test plan steps:
            1. Set test data - set invalid status in one or more proto-tasks
            2. Call Call createCompanyTasks endpoint
            3. verify response
        """
        # Set test data
        file_test_data['json'][0]['status'] = 'DONE'

        # Call createCompanyTasks endpoint
        create_tasks_response = create_company_tasks(assert_response=False, **file_test_data)
        actual_response = create_tasks_response.data
        actual_response.pop('timestamp')
        actual_response.pop('path')
        # verify response
        expected_response = get_expected_response('invalid_status_response', **file_test_data)
        self.assertEqual(400, create_tasks_response.status,
                         format_response(create_tasks_response, 'Test Failed! Unexpected response status'))
        self.assertIn(expected_response["message"], actual_response["message"],
                      format_response(create_tasks_response, 'Test Failed! Unexpected response data'))

    @test_data(file_name="company_tasks_svc/validation_create_company_tasks.json")
    def test_prevent_create_duplicate_task(self, **file_test_data):
        """
        Test Scenario: When a POST call is made to the companytasks endpoint with proto task whose
        companyid, type, and category match an existing task,
        confirm:
            Response status is 400
            Response with error message

        Test Plan steps:
            1. Use test data from prevent_create_duplicate_task.json to POST call the companytasks endpoint
            2. Verify response status and error message
        """
        # Get test data input values to be used by helper functions
        td_endpoint_inputs={}
        td_endpoint_inputs['headers'] = file_test_data['headers']
        td_endpoint_inputs['args'] = file_test_data['args']
        td_endpoint_inputs['json'] = file_test_data['json']
        companyid = td_endpoint_inputs['args']['companyid']

        # Delete pre-existing tasks.
        delete_all_company_tasks(companyid, assert_response=False, **td_endpoint_inputs)

        # Create Task
        successful_create_task_response = create_company_tasks(**td_endpoint_inputs)
        test_task_id = successful_create_task_response.data['content'][0]['id']
        # attempt to create task again via POST Call createcompanytasks endpoint and Verify endpoint response
        response = create_company_tasks(assert_response=False, **td_endpoint_inputs)

        # Verify endpoint response status
        self.assertEqual(400, response.status,
                         format_response(response, 'Test Failed! Unexpected Response Status.'))
        actual_result = response.data

        expected_result = get_expected_response('duplicate_not_allowed', **file_test_data)
        expected_result['errors'][0]['description'] = expected_result['errors'][0]['description'] + test_task_id
        # Verify endpoint response content
        self.assertDictEqual(expected_result, actual_result,
                             format_response(response, 'Test Failed! Unexpected response data'))
        # Delete tasks.
        delete_all_company_tasks(companyid, assert_response=False, **td_endpoint_inputs)

    def _call_endpoint_and_verify_response(self, expected_response_str, **file_test_data):
        # Call createCompanyTasks endpoint
        create_tasks_response = create_company_tasks(assert_response=False, **file_test_data)
        # verify response
        expected_response = get_expected_response(expected_response_str, **file_test_data)
        self.assertEqual(400, create_tasks_response.status,
                         format_response(create_tasks_response, 'Test Failed! Unexpected response status'))
        self.assertDictEqual(expected_response, create_tasks_response.data,
                             format_response(create_tasks_response, 'Test Failed! Unexpected response data'))
