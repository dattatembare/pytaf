import unittest
from lib.get_endpoint import endpoints, call_endpoint
from lib.manage_test_data import test_data, get_expected_response
from lib.utils import format_response

class TestPatchSFDCDataFeed(unittest.TestCase):
    @test_data(file_name="sfdc_svc/sfdc_datafeed/patch_sfdc_datafeed.json")
    def test_patch_sfdc_datafeed_success(self, **testdata):
        """
            This test uses a PATCH call to update an existing client within SFDC with new data.
         validation methodology:
                - The successful endpoint call returns expected status (204)
                - expected data is returned where appropriate.
        """
        # happy path
        response = call_endpoint(endpoints.sfdc_svc.patchsfdcdatafeed, **testdata)
        # verify status code
        self.assertEqual(204, response.status,
                         format_response(response, 'Test Failed! Unexpected Response Status.'))


