from lib.get_endpoint import call_endpoint, endpoints
from lib.utils import format_response, trace

endpoint_inputs = {
    "headers": {
        "Content-Type": "application/json"
    }
}


@trace(text="Delete company tasks")
def delete_tasks(command_args: dict):
    """
    Function compiles a list of tasks associated with a companyid that is supplied to the the deleteCompanyTasks endpoint
    in order to delete all tasks associated with a client
    :return: endpoint call response object
    """
    # Check required argument
    assert command_args.get('companyid'), "Required argument 'companyid' is missing"

    # Find count
    search_args = {"companyid": command_args.get('companyid')}
    endpoint_inputs["args"] = search_args
    endpoint_inputs['json'] = search_args
    count_response = call_endpoint(endpoint_config=endpoints.company_tasks_svc.countCompanyTasks,
                                   command_args=command_args,
                                   **endpoint_inputs)
    actual_count = count_response.data.get('content')
    if actual_count == 0:
        print("Client has no tasks.")
        return
    # Search task Ids
    search_args["pageRequest"] = {"size": actual_count}
    search_response = call_endpoint(endpoint_config=endpoints.company_tasks_svc.getCompanyTasks,
                                    command_args=command_args,
                                    **endpoint_inputs)
    if search_response.status == 404:
        print(search_response.data['errors'][0]['description'])
        return
    # Delete all task Ids
    ids = [company_task['id'] for company_task in search_response.data['content']]
    if ids:
        endpoint_inputs['json'] = ids
        delete_response = call_endpoint(endpoint_config=endpoints.company_tasks_svc.deleteCompanyTasks,
                                        command_args=command_args,
                                        **endpoint_inputs)
        assert search_response.status == 200, f"Delete operation failed! Error: {format_response(delete_response)}"
    print(f"{actual_count} Company tasks deleted successfully! Now, Client has no tasks.")
