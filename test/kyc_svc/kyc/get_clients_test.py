import unittest

from lib import logger
from lib.get_endpoint import endpoints, call_endpoint
from lib.manage_test_data import test_data, get_expected_response
from lib.utils import format_response

log = logger.get_logger()


class TestGetClients(unittest.TestCase):
    @test_data(file_name="kyc_svc/kyc/get_clients.json")
    def test_get_clients(self, **file_test_data):
        """
            This test verifies the results of a get call to the kyc test endpoint
                - The successful endpoint call returns expected status (200)
                - expected client data is returned where appropriate.
        """
        # verify status code
        self._verify_response(expected_status=200, **file_test_data)

    def _verify_response(self, expected_status, **file_test_data):
        # Call kyc_datafeed endpoint
        response = call_endpoint(endpoints.kyc_svc.getkycclients, **file_test_data)
        log.trace(f"response: {response}")

        # Verify endpoint response
        self.assertEqual(expected_status, response.status,
                         format_response(response, 'Test Failed! Unexpected Response Status.'))
        actual_result = response.data

        # only validate the first twenty clients
        del actual_result[20:]

        expected_result = get_expected_response(expected_res='expected_content', **file_test_data)
        self.assertListEqual(expected_result, actual_result,
                             format_response(response, "Test Failed! Unexpected Response."))
