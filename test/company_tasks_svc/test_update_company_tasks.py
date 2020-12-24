import time
import unittest

from lib.manage_test_data import test_data
from lib.utils import format_response
from test.company_tasks_svc.endpoint_call_helpers import delete_all_company_tasks, create_company_tasks, \
    update_company_task, search_company_tasks


class TestCompanyTasksSvcUpdate(unittest.TestCase):

    @test_data(file_name="company_tasks_svc/update_company_tasks.json")
    def test_update_company_tasks_valid(self, **kwargs):
        """
            This test verifies a call to the:
                creatCompanyTasks endpoint can generate tasks associated with a single client
                updateCompanyTasks endpoint can update tasks associated with a single client
                getCompanyTasks endpoint can return a list of tasks associated with a single client
                deleteCompanyTasks endpoint can delete tasks associated with a single client
                countCompanyTasks endpoint can return a count of tasks associated with a single client
            validation methodology:
                The  successfull endpoint call returns expected status (usually 200)
                expected data is returned where appropriate.
        """
        # Grab endpoint inputs from test data kwargs
        td_endpoint_inputs = kwargs['endpoint_inputs']
        companyid = td_endpoint_inputs['args']['companyid']
        ueid = td_endpoint_inputs['args']['ueid']

        # Make sure client has no tasks to start with
        delete_all_company_tasks(companyid, assert_response=False, **td_endpoint_inputs)

        # Create 1 or more Company tasks using information provided by test data file
        create_time = time.strftime("%Y-%m-%d %H:%M",time.gmtime())
        expected_trackingData = {
            "createdByUeid": ueid,
            "updatedByUeid": ueid + "_UPDATE",
            "createdOn": create_time,
            "updatedOn": create_time}
        create_tasks_response = create_company_tasks(**td_endpoint_inputs)
        # create input for update
        ueid = td_endpoint_inputs['args']['ueid'] + '_UPDATE'
        update_tasks = create_tasks_response.data['content'].copy()
        for each_task in update_tasks:
            each_task.pop('trackingData')
        for key, value in each_task.items():
            if key == 'assignees':
                for each_assignee in value:
                    for akey, avalue in each_assignee.items():
                        if each_assignee[akey]:
                            each_assignee[akey] = avalue + '_NEW'
            elif key == 'details':
                for dkey, dvalue in each_task[key].items():
                    each_task[key][dkey] = dvalue + '_NEW'
            elif key == 'status':
                if each_task[key] == 'CREATED':
                    each_task[key] = 'IN_PROGRESS'
                elif each_task[key] == 'IN_PROGRESS':
                    each_task[key] = 'COMPLETED'
                elif each_task[key] == 'COMPLETED':
                    each_task[key] = 'CREATED'
            elif key not in ['id', 'companyid', 'dependencies', 'category', 'type']:
                each_task[key] = each_task[key] + '_NEW'

        # Wait a little before updating newly created task(s)
        time.sleep(60)
        # Update newly created task(s)
        update_company_task(ueid, update_tasks, **td_endpoint_inputs)
        expected_trackingData["updatedOn"] = time.strftime("%Y-%m-%d %H:%M",time.gmtime())
        #  Confirm
        search_args = {"companyid": update_tasks[0]['companyid']}
        search_response = search_company_tasks(search_args, **td_endpoint_inputs)
        expected_tasks = update_tasks
        for each_task in expected_tasks:
            each_task.update({'trackingData': expected_trackingData})
        actual_tasks = search_response.data['content']
        datetimeFormat = '%Y-%m-%dT%H:%M:%S.%f%z'
        for each_task in actual_tasks:
            createdOn = time.strptime(each_task['trackingData']['createdOn'], datetimeFormat)
            createdOn = time.strftime('%Y-%m-%d %H:%M', createdOn)
            each_task['trackingData']['createdOn'] = createdOn
            updatedOn = time.strptime(each_task['trackingData']['updatedOn'], datetimeFormat)
            updatedOn = time.strftime('%Y-%m-%d %H:%M', updatedOn)
            each_task['trackingData']['updatedOn'] = updatedOn

        self.assertListEqual(actual_tasks, expected_tasks, \
                             format_response(search_response, ' Test Failed! Unexpected Response Data.'))
        # Clean up
        delete_all_company_tasks(companyid, **td_endpoint_inputs)
