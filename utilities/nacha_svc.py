from lib.get_endpoint import call_endpoint, endpoints
from lib.utils import trace


@trace(text="Tokenize Bank Account Number")
def tokenize(command_args: dict):
    endpoint_inputs = {}
    tokenize_json = {
        "accountNumber": command_args.get('bank_account_number'),
        "routingNumber": command_args.get('routing_number')
    }
    endpoint_inputs['json'] = [tokenize_json]
    response = call_endpoint(endpoint_config=endpoints.nacha_token_svc.tokenize,
                             command_args=command_args,
                             **endpoint_inputs)
    print(response.data['content'])


@trace(text="Detokenize Bank Account Number")
def detokenize(command_args: dict):
    endpoint_inputs = {}
    tokenize_json = {
        "token": command_args.get('token'),
        "routingNumber": command_args.get('routing_number')
    }
    endpoint_inputs['json'] = [tokenize_json]
    response = call_endpoint(endpoint_config=endpoints.nacha_token_svc.detokenize,
                             command_args=command_args,
                             **endpoint_inputs)
    print(response.data['content'])
