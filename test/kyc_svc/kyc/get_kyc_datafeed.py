import unittest

from lib import logger
from lib.get_endpoint import endpoints, call_endpoint
from lib.manage_test_data import test_data, get_expected_response
from lib.utils import format_response

log = logger.get_logger()


class TestkycDataFeed(unittest.TestCase):
    @test_data(file_name="kyc_svc/kyc/get_kyc_datafeed.json")
    def test_getkycdatafeed_success(self, **file_test_data):
        """
            This test verifies that we can retrieve the KYC client information for an existing client.
                - The successful endpoint call returns expected status (200)
                - expected data is returned where appropriate.
        """
        # verify status code
        self._verify_response(expected_status=200, **file_test_data)

    def _verify_response(self, expected_status, **file_test_data):
        # Call kyc_datafeed endpoint
        response = call_endpoint(endpoints.kyc_svc.getkycclient, **file_test_data)
        log.trace(f"response: {response}")
        # Verify endpoint response
        self.assertEqual(expected_status, response.status,
                         format_response(response, 'Test Failed! Unexpected Response Status.'))
        actual_result = response.data

        expected_result = get_expected_response(expected_res='expected_content', **file_test_data)
        self.assertDictEqual(expected_result, actual_result,
                             format_response(response, "Test Failed! Unexpected Response."))
