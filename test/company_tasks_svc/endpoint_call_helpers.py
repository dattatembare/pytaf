from lib import logger
from lib.get_endpoint import endpoints, call_endpoint
from lib.utils import format_response

log = logger.get_logger()

def create_company_tasks(assert_response=True, **endpoint_inputs):
    """
    Function handles call to creatCompanyTasks endpoint
    :param endpoint_inputs: dictionary containing endpoint call parameters
    :return: endpoint call response object
    """
    create_tasks_response = call_endpoint(endpoints.company_tasks_svc.createCompanyTasks, **endpoint_inputs)
    log.trace(create_tasks_response)
    if assert_response:
        assert create_tasks_response.status == 200, \
            format_response(create_tasks_response, 'Test Failed! Unexpected Response Status.')

    return create_tasks_response


def search_company_tasks(search_args=None, assert_response=True, **endpoint_inputs):
    """
    Function handles call to getCompanyTasks endpoint
    :param endpoint_inputs: dictionary containing endpoint call parameters
    :return: endpoint call response object
    """
    if search_args:
        endpoint_inputs['json'] = search_args
    get_tasks_response = call_endpoint(endpoints.company_tasks_svc.getCompanyTasks, **endpoint_inputs)
    log.trace(get_tasks_response)
    if assert_response:
        assert get_tasks_response.status == 200, \
            format_response(get_tasks_response, 'Test Failed! Unexpected Response Status.')

    return get_tasks_response


def delete_company_tasks(ids_list=None, assert_response=True, **endpoint_inputs):
    """
    Function handles call to deleteCompanyTasks endpoint
    :param endpoint_inputs: dictionary containing endpoint call parameters
    :return: endpoint call response object
    """
    if ids_list:
        endpoint_inputs['json'] = ids_list
    delete_tasks_response = call_endpoint(endpoints.company_tasks_svc.deleteCompanyTasks, **endpoint_inputs)
    if assert_response:
        assert delete_tasks_response.status == 200, \
            format_response(delete_tasks_response, 'Test Failed! Unexpected Response Status.')

    return delete_tasks_response


def count_company_tasks(companyid=None, **endpoint_inputs):
    """
    Function handles call to countCompanyTasks endpoint
    :param endpoint_inputs: dictionary containing endpoint call parameters
    :return: endpoint call response object
    """
    if companyid:
        endpoint_inputs['args']['companyid'] = companyid
    endpoint_inputs['json'] = {"companyid": companyid}
    count_tasks_response = call_endpoint(endpoints.company_tasks_svc.countCompanyTasks, **endpoint_inputs)
    assert count_tasks_response.status == 200, \
        format_response(count_tasks_response, 'Test Failed! Unexpected Response Status.')

    return count_tasks_response


def delete_all_company_tasks(companyid, **endpoint_inputs):
    """
    Function compiles a list of tasks associated with a companyid that is suplied to the the deleteCompanyTasks endpoint
    inorder to delete all tasks associated with a client
    :param endpoint_inputs: dictionary containing endpoint call parameters
    :return: endpoint call response object
    """
    # Search tasks
    count_tasks_response = count_company_tasks(companyid, **endpoint_inputs)
    actual_count = count_tasks_response.data.get('content')
    company_tasks_list = {}
    if actual_count:
        search_args = {"companyid": companyid, "pageRequest": {"size": actual_count}}
        search_tasks_response = search_company_tasks(search_args, **endpoint_inputs)
        company_tasks_list = search_tasks_response.data['content'].copy()
    if company_tasks_list:
        ids = [company_task['id'] for company_task in company_tasks_list]
        delete_company_tasks(ids, **endpoint_inputs)
    count_tasks_response = count_company_tasks(companyid, **endpoint_inputs)
    actual_count = count_tasks_response.data.get('content')
    assert actual_count == 0, \
        format_response(count_tasks_response, 'Test Failed! Unexpected Response Data.')


def update_company_task(ueid=None, update_args=None, assert_response=True, **endpoint_inputs):
    """
    Function handles call to updateCompanyTasks endpoint
    :param endpoint_inputs: dictionary containing endpoint call parameters
    :return: endpoint call response object
    """
    if update_args:
        endpoint_inputs['json'] = update_args
    if ueid:
        endpoint_inputs['args']['ueid'] = ueid
    update_tasks_response = call_endpoint(endpoints.company_tasks_svc.updateCompanyTasks, **endpoint_inputs)
    log.trace(update_tasks_response)
    if assert_response:
        assert update_tasks_response.status == 200, \
            format_response(update_tasks_response, 'Test Failed! Unexpected Response Status.')

    return update_tasks_response
