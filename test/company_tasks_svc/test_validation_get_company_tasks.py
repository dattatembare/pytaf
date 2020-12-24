import unittest

from lib.manage_test_data import test_data, get_expected_response
from lib.utils import format_response
from test.company_tasks_svc.endpoint_call_helpers import search_company_tasks


class TestValidationGetCompanyTasksSvc(unittest.TestCase):

    @test_data(file_name="company_tasks_svc/validation_get_company_tasks.json")
    def test_company_tasks_error_when_companyid_not_match(self, **file_test_data):
        """
        Scenario:
            When the getCompanyTasks endpoint is called and the companyid in URL does not match companyid in one or more
            proto-tasks in endpoint inputs, confirm:
                Response contains Status code 400
                error is reported
                no tasks are created
        Test plan steps:
            1. Set test data - companyid in URL does not match companyid in one or more proto-tasks
            2. Call Call getCompanyTasks endpoint
            3. verify response
        """
        # Set test data
        _search_args = {"companyid": 'SOMEOTHEREcompanyid'}

        # Call getCompanyTasks endpoint
        get_tasks_response = search_company_tasks(_search_args, assert_response=False, **file_test_data)
        # verify response
        expected_response = get_expected_response('invalid_companyid_response', **file_test_data)
        self.assertEqual(400, get_tasks_response.status,
                         format_response(get_tasks_response, 'Test Failed! Unexpected response status'))
        self.assertDictEqual(expected_response, get_tasks_response.data,
                             format_response(get_tasks_response, 'Test Failed! Unexpected response data'))
