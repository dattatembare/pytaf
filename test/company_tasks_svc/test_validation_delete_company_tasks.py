import copy
import unittest

from lib.manage_test_data import test_data, get_expected_response
from lib.utils import format_response
from test.company_tasks_svc.endpoint_call_helpers import create_company_tasks, delete_company_tasks


class TestValidationDeleteCompanyTasksSvc(unittest.TestCase):

    @test_data(file_name="company_tasks_svc/validation_delete_company_tasks.json")
    def setUp(self, **file_test_data):
        """
        Create one task for update operations
        :return:
        """
        self._test_data = file_test_data
        self.create_tasks_response = create_company_tasks(**file_test_data)
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
            When the deleteCompanyTasks endpoint is called and the companyid in URL does not match companyid in one or more
            proto-tasks in endpoint inputs, confirm:
                Response contains Status code 400
                error is reported
                no tasks are created
        Test plan steps:
            1. Create new company task to do delete operation
            2. Set test data to update operation- companyid in URL does not match companyid in one or more proto-tasks
            3. Call Call deleteCompanyTasks endpoint
            4. verify response
            5. Delete created company task
        """

        # Set test data
        delete_data = copy.deepcopy(self._test_data)
        delete_data['args']['companyid'] = 'SOMEOTHEREcompanyid'

        # Call getCompanyTasks endpoint
        delete_tasks_response = delete_company_tasks([self._id], assert_response=False, **delete_data)
        # verify response
        expected_response = get_expected_response('invalid_companyid_response', **self._test_data)
        self.assertEqual(400, delete_tasks_response.status,
                         format_response(delete_tasks_response, 'Test Failed! Unexpected response status'))
        self.assertDictEqual(expected_response, delete_tasks_response.data,
                             format_response(delete_tasks_response, 'Test Failed! Unexpected response data'))
