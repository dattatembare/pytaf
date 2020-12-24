import unittest

from lib.manage_test_data import test_data
from test.company_tasks_svc.endpoint_call_helpers import create_company_tasks


class TestCompanyTasksSvcUpdate(unittest.TestCase):

    @test_data(file_name="company_tasks_svc/add_company_tasks.json")
    def test_add_company_tasks_valid(self, **kwargs):
        """
            This test adds tasks to 1 or more clients provided required client companyids and UEIDs and optional Assignees:
                Each Task's companyid will be updated to the companyid provided,
                If assignees is provide with companyid then Each Task's assignees will be updated to the assignees provided,
                Else each tasks assignee will be set to one with the the ueid provided with the companyid
        """
        # Grab endpoint inputs from test data kwargs
        for each_client in kwargs['client_records']:
            companyid = each_client['args']['companyid']
            ueid = each_client['args']['ueid']
            assignees = each_client['args']['assignees'] if each_client['args'].get('assignees') else [{'ueid': ueid}]
            # create endpoint_inputs dictionary for endpoint calls
            endpoint_inputs = {}
            endpoint_inputs['headers'] = kwargs['headers']
            endpoint_inputs['args'] = {'companyid': companyid, 'ueid': ueid}
            endpoint_inputs['json'] = kwargs['json']
            # update tasks in json
            for each_task in endpoint_inputs['json']:
                each_task['assignees'] = assignees
                each_task['companyid'] = companyid
            create_company_tasks(**endpoint_inputs)
