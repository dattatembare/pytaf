import unittest
from lib.get_endpoint import endpoints, call_endpoint
from lib.manage_test_data import test_data, get_expected_response
from lib.utils import format_response


class TestSFDCVersions(unittest.TestCase):

    def test_sfdc_versions_success(self, **testdata):
        """
            This tests verifies the health of the SFDC service via a call to version endpoint
         validation methodology:
                - The  successfull endpoint call returns expected status (usually 200)
                - expected data is returned where appropriate.
        """
        # happy path
        response = call_endpoint(endpoints.sfdc_svc.sfdcversions, **testdata)
        # verify status code
        self.assertEqual(200, response.status,
                         format_response(response, 'Test Failed! Unexpected Response Status.'))
