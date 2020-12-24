import unittest

from lib import logger
from lib.get_endpoint import endpoints, call_endpoint
from lib.manage_test_data import test_data, get_expected_response
from lib.utils import format_response


class TestSfdcDataFeed(unittest.TestCase):
    @test_data(file_name="sfdc_svc/sfdc_datafeed/get_sfdc_datafeed.json")
    def test_get_sfdc_datafeed_success(self, **file_test_data):
        """
            This test verifies the health of the 1st SFDC Data Feed call.
                - The successful endpoint call returns expected status (200)
                - expected data is returned where appropriate.
        """
        # verify status code
        self._verify_response(expected_status=200, **file_test_data)

    def _verify_response(self, expected_status, **file_test_data):
        # Call sfdc_datafeed endpoint
        response = call_endpoint(endpoints.sfdc_svc.getsfdcdatafeed, **file_test_data)

        # Verify endpoint response
        self.assertEqual(expected_status, response.status,
                         format_response(response, 'Test Failed! Unexpected Response Status.'))
        actual_result = response.data
        # Remove uncertain fields from response
        del actual_result['LastViewedDate']
        del actual_result['LastReferencedDate']
        expected_result = get_expected_response(expected_res='expected_content', **file_test_data)
        self.assertDictEqual(expected_result, actual_result,
                             format_response(response, "Test Failed! Unexpected Response."))
