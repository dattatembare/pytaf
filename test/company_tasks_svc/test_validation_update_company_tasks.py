import copy
import unittest

from lib.manage_test_data import test_data, get_expected_response
from lib.utils import format_response
from test.company_tasks_svc.endpoint_call_helpers import update_company_task, create_company_tasks, delete_company_tasks


class TestValidationUpdateCompanyTasksSvc(unittest.TestCase):

    @test_data(file_name="company_tasks_svc/validation_update_company_tasks.json")
    def setUp(self, **file_test_data):
        """
        Create one task for update operations
        :return:
        """
        self._test_data = file_test_data
        self.create_tasks_response = create_company_tasks(assert_response=False, **file_test_data)
        self._id = self.create_tasks_response.data['content'][0]['id']

    def tearDown(self):
        """
        Delete created task after update tests
        :return:
        """
        delete_company_tasks([self._id], **self._test_data)

    def test_company_tasks_error_when_companyid_not_match(self):
        """
        Scenario:
            When the updateCompanyTasks endpoint is called and the companyid in URL does not match companyid in one or more
            proto-update-tasks in endpoint inputs, confirm:
                Response contains Status code 400
                error is reported
                no tasks are created
        Test plan steps:
            1. Create new company task to do update operation
            2. Set test data - companyid in URL does not match companyid in one or more proto-tasks
            3. Call Call updateCompanyTasks endpoint
            4. verify response
            5. Delete created company task
        """
        # Set test data
        update_data = self.create_tasks_response.data['content']
        update_data[0]['companyid'] = 'SOMEOTHEREcompanyid'
        self._test_data['json'] = update_data

        # Call update task endpoint and verify
        self._call_endpoint_and_verify_response('invalid_companyid_response', **self._test_data)

    def test_company_tasks_error_when_required_field_missing(self):
        """
        Scenario:
            When the updateCompanyTasks endpoint is called and One or more proto-update-tasks in endpoint inputs is
            missing required field(s) [companyid, id], confirm:
                Response contains Status code 400
                error is reported in data
                no tasks are created
        Test plan steps:
            1. Create new company task to do update operation
            2. Set test data - remove companyid/id from task
            3. Call Call updateCompanyTasks endpoint
            4. verify response
            5. Delete created company task
        """
        # Set test data
        update_data = copy.deepcopy(self.create_tasks_response.data['content'])
        update_data[0].pop('companyid')
        self._test_data['json'] = update_data

        # Call update task endpoint and verify
        self._call_endpoint_and_verify_response('invalid_companyid_response', **self._test_data)

        # Set test data
        update_data = copy.deepcopy(self.create_tasks_response.data['content'])
        update_data[0].pop('id')
        self._test_data['json'] = update_data

        # Call update task endpoint and verify
        self._call_endpoint_and_verify_response('missing_companyid_response', **self._test_data)

    def test_company_tasks_error_when_invalid_id(self):
        """
        Scenario:
            When the updateCompanyTasks endpoint is called and , One or more proto-update-tasks in endpoint inputs has
            an invalid id, confirm:
                Response contains Status code 400
                error is reported
                no tasks are created
        Test plan steps:
            1. Create new company task to do update operation
            2. Set test data - set invalid id task
            3. Call Call updateCompanyTasks endpoint
            4. verify response
            5. Delete created company task
        """
        # Set test data
        update_data = self.create_tasks_response.data['content']
        update_data[0]['id'] = 'INVALID-ID'
        self._test_data['json'] = update_data

        # Call update task endpoint and verify
        self._call_endpoint_and_verify_response('invalid_id_response', 404, **self._test_data)

    @test_data(file_name="company_tasks_svc/validation_update_company_tasks_2.json")
    def test_company_tasks_error_when_id_of_other_companyid(self, **test_data_new_task):
        """
        Scenario:
            When the updateCompanyTasks endpoint is called and , One or more proto-update-tasks in endpoint inputs
            with an id that maps to an existing task with a different companyid, confirm:
                Response contains Status code 400
                error is reported
                no tasks are created
        Test plan steps:
            1. Create new company task to do update operation
            2. Set test data - set invalid id task
            3. Call Call updateCompanyTasks endpoint
            4. verify response
            5. Delete created company task
        """
        # Create one more task, i.e task 2
        new_create_tasks_response = create_company_tasks(assert_response=False, **test_data_new_task)

        # Set test data
        update_data = self.create_tasks_response.data['content']
        # Using companyid of task 1 with id of task 2
        update_data[0]['id'] = new_create_tasks_response.data['content'][0]['id']
        self._test_data['json'] = update_data

        # Call update task endpoint and verify
        self._call_endpoint_and_verify_response('id_of_other_companyid_response', 400, **self._test_data)

    def test_company_tasks_error_when_empty_assignees(self):
        """
        Scenario:
            When the updateCompanyTasks endpoint is called and One or more proto-tasks in endpoint inputs with one or
            more empty assignees, confirm:
                Response contains Status code 400
                error is reported in data
                no tasks are created
        Test plan steps:
            1. Create new company task to do update operation
            2. Set test data - delete assignees from task
            3. Call Call updateCompanyTasks endpoint
            4. verify response
            5. Delete created company task
        """
        # Set test data
        update_data = self.create_tasks_response.data['content']
        assignees = update_data[0]['assignees']
        assignees.append({})
        update_data[0]['assignees'] = assignees
        self._test_data['json'] = update_data

        # Call update task endpoint and verify
        self._call_endpoint_and_verify_response('empty_assignees_response', **self._test_data)

    def test_company_tasks_error_when_invalid_status(self):
        """
        Scenario:
            When the updateCompanyTasks endpoint is called and One or more proto-tasks in endpoint inputs with a status
            not in the list: [CREATED, COMPLETED, IN_PROGRESS] , confirm:
                Response contains Status code 400
                error is reported in data
                no tasks are created
        Test plan steps:
            1. Create new company task to do update operation
            2. Set test data - set invalid status in task
            3. Call Call updateCompanyTasks endpoint
            4. verify response
            5. Delete created company task
        """
        # Set test data
        update_data = self.create_tasks_response.data['content']
        update_data[0]['status'] = 'DONE'
        self._test_data['json'] = update_data

        # Call updateCompanyTasks endpoint
        update_tasks_response = update_company_task(assert_response=False, **self._test_data)
        actual_response = update_tasks_response.data
        actual_response.pop('timestamp')
        actual_response.pop('path')
        # verify response
        expected_response = get_expected_response('invalid_status_response', **self._test_data)
        self.assertEqual(400, update_tasks_response.status,
                         format_response(update_tasks_response, 'Test Failed! Unexpected response status'))
        self.assertIn(expected_response["message"], actual_response["message"],
                             format_response(update_tasks_response, 'Test Failed! Unexpected response data'))

    def test_company_tasks_error_when_update_type(self):
        """
        Scenario:
            When the updateCompanyTasks endpoint is called to update the type of a task,
            confirm:
                Response contains Status code 400
                error is reported
                no tasks are created
        Test plan steps:
            1. Create new company task to do update operation on
            2. Set test data - new type in one or more proto-tasks
            3. Call updateCompanyTasks endpoint
            4. verify response
            5. Delete created company task
        """
        # Set test data
        update_data = self.create_tasks_response.data['content']
        update_data[0]['type'] = 'SOMEOTHERETYPE'
        self._test_data['json'] = update_data

        # Call update task endpoint and verify
        self._call_endpoint_and_verify_response('update_type_response', **self._test_data)

    def test_company_tasks_error_when_update_category(self):
        """
        Scenario:
            When the updateCompanyTasks endpoint is called to update the category of a task,
            confirm:
                Response contains Status code 400
                error is reported
                no tasks are created
        Test plan steps:
            1. Create new company task to do update operation on
            2. Set test data - new category in one or more proto-tasks
            3. Call updateCompanyTasks endpoint
            4. verify response
            5. Delete created company task
        """
        # Set test data
        update_data = self.create_tasks_response.data['content']
        update_data[0]['category'] = 'SOMEOTHERECAT'
        self._test_data['json'] = update_data

        # Call update task endpoint and verify
        self._call_endpoint_and_verify_response('update_category_response', **self._test_data)

    def test_company_tasks_error_when_update_companyid(self):
        """
        Scenario:
            When the updateCompanyTasks endpoint is called to update the companyid of a task,
            confirm:
                Response contains Status code 400
                error is reported
                no tasks are created
        Test plan steps:
            1. Create new company task to do update operation on
            2. Set test data - new companyid in URL and in one or more proto-tasks
            3. Call updateCompanyTasks endpoint
            4. verify response
            5. Delete created company task
        """
        # Set test data
        # making a copy so as to not corrupt self._test_data needed for clean up
        test_data_copy = copy.deepcopy(self._test_data)
        test_data_copy['args']['companyid'] = 'SOMEOTHEREcompanyid'
        update_data = self.create_tasks_response.data['content']
        update_data[0]['companyid'] = 'SOMEOTHEREcompanyid'
        test_data_copy['json'] = update_data

        # Call update task endpoint and verify
        self._call_endpoint_and_verify_response('update_companyid_response', **test_data_copy)

    def _call_endpoint_and_verify_response(self, expected_response_str, expected_status_code=400, **file_test_data):
        # Call updateCompanyTasks endpoint
        update_tasks_response = update_company_task(assert_response=False, **file_test_data)
        # verify response
        expected_response = get_expected_response(expected_response_str, **file_test_data)
        self.assertEqual(expected_status_code, update_tasks_response.status,
                         format_response(update_tasks_response, 'Test Failed! Unexpected response status'))
        self.assertDictEqual(expected_response, update_tasks_response.data,
                             format_response(update_tasks_response, 'Test Failed! Unexpected response data'))
