import unittest
from lib.get_endpoint import endpoints, call_endpoint
from lib.manage_test_data import test_data, get_expected_response
from lib.utils import format_response

class TestCompanyTasksSvcHealth(unittest.TestCase):
    @test_data(file_name="company_tasks_svc/company_tasks_health_check.json")
    def test_health_check_success(self, **testdata):
        """
            This tests verifies the health of the Company Tasks service via a call to health endpoint
         validation methodology:
                - The  successfull endpoint call returns expected status (usually 200)
                - expected data is returned where appropriate.
        """
        response = call_endpoint(endpoints.company_tasks_svc.health)
        self.assertEqual(200, response.status, format_response(response, 'Test Failed! Unexpected Response Status.'))
        actual_result = response.data
        del actual_result['details']['diskSpace']['details']
        del actual_result['details']['mongo']['details']
        expected_status = get_expected_response(expected_res='expected_status', **testdata)
        self.assertDictEqual(expected_status, actual_result,
                             format_response(response,"Test Failed! Unexpected Response."))

