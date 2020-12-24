import unittest

from lib.manage_test_data import test_data
from lib.utils import format_response
from test.company_tasks_svc.endpoint_call_helpers import delete_all_company_tasks, create_company_tasks, \
    search_company_tasks


class TestCompanyTasksSvcSearch(unittest.TestCase):

    @test_data(file_name="company_tasks_svc/search_company_tasks.json")
    def test_search_company_tasks_valid(self, **kwargs):
        """
        This test verifies a call to the getCompanyTasks endpoint:
            - Requires
                - a single companyid be supplied in the endpoint call path (for auth)
                - a single companyid be supplied in the search arguments
            - Can return a list of tasks when provided a single companyid
            - Will return tasks associated with a client/companyid that match the values provided
              singly or as a list of the following task elements
                - ids
                - categories
                - types
                - statuses
                - ueids
                - advSecGuids
            - When not provided Pagination arguments will by default return:
                    - a list of no more than 10 tasks sorted by id
                    - Total number of tasks matching search arguments
            - When provided a number of tasks will return
                    - a list of no more than that number of tasks sorted by id
            - When provided an offset will return
                    - a list of no more than the prescribed number of tasks
                      starting with the task in the list position provided
        validation methodology:
            The  successful endpoint call returns expected status (usually 200)
            expected data is returned where appropriate.
        """
        # Grab endpoint inputs from test data kwargs
        td_endpoint_inputs = kwargs['endpoint_inputs']
        companyid = td_endpoint_inputs['args']['companyid']
        required_search_args = {"companyid": companyid}

        # Make sure client has no tasks to start with
        delete_all_company_tasks(companyid, **td_endpoint_inputs)

        # Create multiple Company tasks using information provided by test data file
        create_tasks_response = create_company_tasks(**td_endpoint_inputs)
        test_tasks_list = create_tasks_response.data['content']

        # Search by companyid
        # Call getCompanyTasks endpoint
        search_response = search_company_tasks(required_search_args, **td_endpoint_inputs)

        # Confirm Search by companyid returns upto 10 matches by default
        expected_task_list = test_tasks_list
        for each_task in expected_task_list:
            each_task.pop('trackingData')
        actual_task_list = search_response.data['content']
        for each_task in actual_task_list:
            each_task.pop('trackingData')
        self.assertListEqual(actual_task_list, expected_task_list[0:10],
                             format_response(search_response, ' Test Failed! Unexpected Response Data.'))

        # Confirm Search (by companyid) can return a second page of tasks
        search_page2 = {"pageRequest": {"page": 1}}
        # Call getCompanyTasks endpoint
        search_response = search_company_tasks({**required_search_args, **search_page2}, **td_endpoint_inputs)
        actual_task_list = search_response.data['content']
        for each_task in actual_task_list:
            each_task.pop('trackingData')
        self.assertListEqual(actual_task_list, expected_task_list[10:20],
                             format_response(search_response, ' Test Failed! Unexpected Response Data.'))

        # Confirm Search by companyid can return all tasks
        search_all = {"pageRequest": {"size": len(test_tasks_list)}}
        # Call getCompanyTasks endpoint
        search_response = search_company_tasks({**required_search_args, **search_all}, **td_endpoint_inputs)
        actual_task_list = search_response.data['content']
        for each_task in actual_task_list:
            each_task.pop('trackingData')
        self.assertListEqual(actual_task_list, expected_task_list,
                             format_response(search_response, ' Test Failed! Unexpected Response Data.'))

        # Search by ID
        ids = [test_task['id'] for test_task in test_tasks_list]
        search_id = {"ids": ids[0:len(ids) - 2]}
        # Call getCompanyTasks endpoint
        search_response = search_company_tasks({**required_search_args, **search_id}, **td_endpoint_inputs)
        # Confirm Search by id returns expected tasks
        expected_task_list = self._search_list_of_tasks({**required_search_args, **search_id}, *test_tasks_list)
        actual_task_list = search_response.data['content']
        for each_task in actual_task_list:
            each_task.pop('trackingData')
        self.assertListEqual(actual_task_list, expected_task_list[0:10],
                             format_response(search_response, ' Test Failed! Unexpected Response Data.'))

        # Search by category
        # Get list of unique Categories
        unique_cats = list({test_task['category'] for test_task in test_tasks_list})
        search_cat = {"categories": [unique_cats[1]]}
        expected_task_list = self._search_list_of_tasks({**required_search_args, **search_cat}, *test_tasks_list)
        # Call getCompanyTasks endpoint
        search_response = search_company_tasks({**required_search_args, **search_cat}, **td_endpoint_inputs)

        # Confirm Search by category returns expected tasks
        actual_task_list = search_response.data['content']
        for each_task in actual_task_list:
            each_task.pop('trackingData')
        self.assertListEqual(actual_task_list, expected_task_list[0:10],
                             format_response(search_response, ' Test Failed! Unexpected Response Data.'))

        # Search by type
        # Get list of unique types
        unique_types = list({test_task['type'] for test_task in test_tasks_list})
        search_type = {"types": unique_types[0:2]}
        expected_task_list = self._search_list_of_tasks({**required_search_args, **search_type}, *test_tasks_list)
        # Call getCompanyTasks endpoint
        search_response = search_company_tasks({**required_search_args, **search_type}, **td_endpoint_inputs)

        # Confirm Search by type returns expected tasks
        actual_task_list = search_response.data['content']
        for each_task in actual_task_list:
            each_task.pop('trackingData')
        self.assertListEqual(actual_task_list, expected_task_list[0:10],
                             format_response(search_response, ' Test Failed! Unexpected Response Data.'))

        # Search by status
        # Get list of unique statuses
        unique_statuses = list({test_task['status'] for test_task in test_tasks_list})
        search_status = {"statuses": unique_statuses[0:2]}
        expected_task_list = self._search_list_of_tasks({**required_search_args, **search_status}, *test_tasks_list)
        # Call getCompanyTasks endpoint
        search_response = search_company_tasks({**required_search_args, **search_status}, **td_endpoint_inputs)

        # Confirm Search by status returns expected tasks
        actual_task_list = search_response.data['content']
        for each_task in actual_task_list:
            each_task.pop('trackingData')
        self.assertListEqual(actual_task_list, expected_task_list[0:10],
                             format_response(search_response, ' Test Failed! Unexpected Response Data.'))

        # Search by advSecGuid
        # Get list of unique advSecGuids
        unique_advSecGuids = []
        for assignee_list in [test_task['assignees'] for test_task in test_tasks_list]:
            for rl in [assignee['advSecGuid'] for assignee in assignee_list]:
                # check if exists in unique list or not
                if rl and rl not in unique_advSecGuids:
                    unique_advSecGuids.append(rl)
        search_advSecGuid = {"advSecGuids": unique_advSecGuids[0:2]}
        expected_task_list = self._search_list_of_tasks({**required_search_args, **search_advSecGuid}, *test_tasks_list)
        # Call getCompanyTasks endpoint
        search_response = search_company_tasks({**required_search_args, **search_advSecGuid}, **td_endpoint_inputs)

        # Confirm Search by advSecGuid returns expected tasks
        actual_task_list = search_response.data['content']
        for each_task in actual_task_list:
            each_task.pop('trackingData')
        self.assertListEqual(actual_task_list, expected_task_list[0:10],
                             format_response(search_response, ' Test Failed! Unexpected Response Data.'))

        # Search by ueid
        # Get list of unique advSecGuids
        unique_ueids = []
        for assignee_list in [test_task['assignees'] for test_task in test_tasks_list]:
            for ue in [assignee['ueid'] for assignee in assignee_list]:
                # check if exists in unique list or not
                if ue and ue not in unique_ueids:
                    unique_ueids.append(ue)
        search_ueid = {"ueids": unique_ueids[0:2]}
        expected_task_list = self._search_list_of_tasks({**required_search_args, **search_ueid}, *test_tasks_list)
        # Call getCompanyTasks endpoint
        search_response = search_company_tasks({**required_search_args, **search_ueid}, **td_endpoint_inputs)
        # Confirm Search by ueid returns expected tasks
        actual_task_list = search_response.data['content']
        for each_task in actual_task_list:
            each_task.pop('trackingData')
        self.assertListEqual(actual_task_list, expected_task_list[0:10],
                             format_response(search_response, ' Test Failed! Unexpected Response Data.'))

        # Search by multiple elements
        search_type = {'types': ['bank_info', 'business_info']}
        search_ueid = {'ueids': ['u2', 'u4']}
        search_cat = {'categories': ['onboarding']}
        search_multiple = {**required_search_args, **search_type, **search_ueid, **search_cat}
        expected_task_list = self._search_list_of_tasks(search_multiple, *test_tasks_list)
        # Call getCompanyTasks endpoint
        search_response = search_company_tasks(search_multiple, **td_endpoint_inputs)

        # Confirm Search by ueid returns expected tasks
        actual_task_list = search_response.data['content']
        for each_task in actual_task_list:
            each_task.pop('trackingData')
        self.assertListEqual(actual_task_list, expected_task_list[0:10],
                             format_response(search_response, ' Test Failed! Unexpected Response Data.'))

        # Clean up
        delete_all_company_tasks(companyid, **td_endpoint_inputs)

    def _search_list_of_tasks(self, search_args, *company_task_list):
        """
        This function provides a list of tasks to compare against tasks returned from search endpoint call
        :param search_args:
        :param task_list:
        :return: List of company tasks that match search args
        """
        # search_args_no_pagerequest = search_args.copy()
        if search_args.get('pageRequest'):
            search_args.pop('pageRequest')

        if not search_args.get('companyid'):
            return []

        # Find matching tasks
        list_of_tasks_that_match = []
        search_arg_to_task = {'ids': 'id', 'categories': 'category', 'types': 'type', 'statuses': 'status',
                              'ueids': 'ueid', 'advSecGuids': 'advSecGuid'}
        tasks_to_search_args = {'id': 'ids', 'category': 'categories', 'type': 'types', 'status': 'statuses',
                                'ueid': 'ueids', 'advSecGuid': 'advSecGuids'}
        for each_task in company_task_list:
            for key, value in each_task.items():
                if key not in ['companyid', 'assignees', 'details', 'dependencies']:
                    if search_args.get(tasks_to_search_args[key]) and value in search_args.get(
                            tasks_to_search_args[key]):
                        if each_task not in list_of_tasks_that_match:
                            list_of_tasks_that_match.append(each_task)
                elif key == 'assignees' and 'advSecGuids' in search_args.keys():
                    for each_assignee in value:
                        match_found = False
                        for akey, avalue in each_assignee.items():
                            if match_found:
                                continue
                            elif akey == 'advSecGuid' and avalue in search_args['advSecGuids']:
                                if each_task not in list_of_tasks_that_match:
                                    list_of_tasks_that_match.append(each_task)
                                    match_found = True
                elif key == 'assignees' and 'ueids' in search_args.keys():
                    for each_assignee in value:
                        match_found = False
                        for akey, avalue in each_assignee.items():
                            if match_found:
                                continue
                            elif akey == 'ueid' and avalue in search_args['ueids']:
                                if each_task not in list_of_tasks_that_match:
                                    list_of_tasks_that_match.append(each_task)
                                    match_found = True

        # Remove tasks that do not match all criteria
        search_args_no_companyid = search_args.copy()
        search_args_no_companyid.pop('companyid')
        new_list = list_of_tasks_that_match.copy()
        for each_task in list_of_tasks_that_match:
            for skey, svalue in search_args_no_companyid.items():
                if skey == 'advSecGuids':
                    # make list of advSecGuids
                    assignee_advSecGuids = []
                    for each_assignee in each_task['assignees']:
                        if each_assignee['advSecGuid'] and each_assignee['advSecGuid'] in svalue:
                            if each_assignee['advSecGuid'] not in assignee_advSecGuids:
                                assignee_advSecGuids.append(each_assignee['advSecGuid'])
                    if not assignee_advSecGuids:
                        # list_of_tasks_that_match.remove(each_task)
                        if each_task in new_list:
                            new_list.remove(each_task)
                    elif not list(set(assignee_advSecGuids) & set(svalue)):
                        # list_of_tasks_that_match.remove(each_task)
                        if each_task in new_list:
                            new_list.remove(each_task)
                elif skey == 'ueids':
                    # make list of ueids
                    assignee_ueids = []
                    for each_assignee in each_task['assignees']:
                        if each_assignee['ueid'] and each_assignee['ueid'] in svalue:
                            if each_assignee['ueid'] not in assignee_ueids:
                                assignee_ueids.append(each_assignee['ueid'])
                        if not list(set(assignee_ueids) & set(svalue)):
                            if each_task in new_list:
                                new_list.remove(each_task)
                elif each_task[search_arg_to_task[skey]] not in svalue:
                    # list_of_tasks_that_match.remove(each_task)
                    if each_task in new_list:
                        new_list.remove(each_task)
                list_of_tasks_that_match = new_list
        return list_of_tasks_that_match
