"""Web Service Client library"""
import inspect
import json
import sys
from json import JSONDecodeError

import requests
import urllib3
# Disables warning message in python output
from requests import Response

from lib.common_namedtuples import HttpResponse, EndPoint, transaction-id, NO_VALUE

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SERVER_ERROR_STATUS = '555'


def delete(endpoint: EndPoint) -> HttpResponse:
    """
    Execute delete request
    :param endpoint: EndPoint object
    :return: HttpResponse object
    """
    if endpoint.json:
        # Note(requests documentation), the json parameter is ignored if either data or files is passed.
        try:
            response = requests.delete(
                endpoint.uri,
                headers=endpoint.headers,
                params=endpoint.params,
                json=endpoint.json,
                verify=False
            )
        except Exception as e:
            return HttpResponse(env=endpoint.env, url=endpoint.uri, status=SERVER_ERROR_STATUS, error=e)
    else:
        try:
            response = requests.delete(
                endpoint.uri,
                data=endpoint.data,
                headers=endpoint.headers,
                params=endpoint.params,
                files=endpoint.files,
                verify=False
            )
        except Exception as e:
            return HttpResponse(env=endpoint.env, url=endpoint.uri, status=SERVER_ERROR_STATUS, error=e)
    return send_response(endpoint, response)


def get(endpoint: EndPoint) -> HttpResponse:
    """
    :param endpoint: EndPoint object
    :return: HttpResponse object
    """
    try:
        response = requests.get(
            endpoint.uri,
            headers=endpoint.headers,
            params=endpoint.params,
            verify=False
        )
    except Exception as e:
        return HttpResponse(env=endpoint.env, url=endpoint.uri, status=SERVER_ERROR_STATUS, error=e)

    return send_response(endpoint, response)


def post(endpoint: EndPoint) -> HttpResponse:
    """
    :param endpoint: EndPoint object
    :return: HttpResponse object
    """
    if endpoint.json is not None:
        # Note(requests documentation), the json parameter is ignored if either data or files is passed.
        try:
            response = requests.post(
                endpoint.uri,
                headers=endpoint.headers,
                params=endpoint.params,
                json=endpoint.json,
                verify=False
            )
        except Exception as e:
            return HttpResponse(env=endpoint.env, url=endpoint.uri, status=SERVER_ERROR_STATUS, error=e)

    else:
        try:
            response = requests.post(
                endpoint.uri,
                data=endpoint.data,
                headers=endpoint.headers,
                params=endpoint.params,
                files=endpoint.files,
                verify=False
            )
        except Exception as e:
            return HttpResponse(env=endpoint.env, url=endpoint.uri, status=SERVER_ERROR_STATUS, error=e)

    return send_response(endpoint, response)


def patch(endpoint: EndPoint) -> HttpResponse:
    """
    :param endpoint: EndPoint object
    :return: HttpResponse object
    """
    if endpoint.json:
        # Note(requests documentation), the json parameter is ignored if either data or files is passed.
        try:
            response = requests.patch(
                endpoint.uri,
                headers=endpoint.headers,
                params=endpoint.params,
                json=endpoint.json,
                verify=False
            )
        except Exception as e:
            return HttpResponse(env=endpoint.env, url=endpoint.uri, status=SERVER_ERROR_STATUS, error=e)
    else:
        try:
            response = requests.patch(
                endpoint.uri,
                data=endpoint.data,
                headers=endpoint.headers,
                params=endpoint.params,
                files=endpoint.files,
                verify=False
            )
        except Exception as e:
            return HttpResponse(env=endpoint.env, url=endpoint.uri, status=SERVER_ERROR_STATUS, error=e)
    return send_response(endpoint, response)


def put(endpoint: EndPoint) -> HttpResponse:
    """
    :param endpoint: EndPoint object
    :return: HttpResponse object
    """
    if endpoint.json is not None:
        # Note(requests documentation), the json parameter is ignored if either data or files is passed.
        try:
            response = requests.put(
                endpoint.uri,
                headers=endpoint.headers,
                params=endpoint.params,
                json=endpoint.json,
                verify=False
            )
        except Exception as e:
            return HttpResponse(env=endpoint.env, url=endpoint.uri, status=SERVER_ERROR_STATUS, error=e)
    else:
        try:
            response = requests.put(
                endpoint.uri,
                data=endpoint.data,
                headers=endpoint.headers,
                params=endpoint.params,
                files=endpoint.files,
                verify=False
            )
        except Exception as e:
            return HttpResponse(env=endpoint.env, url=endpoint.uri, status=SERVER_ERROR_STATUS, error=e)
    return send_response(endpoint, response)


def send_response(endpoint: EndPoint, response: Response) -> HttpResponse:
    """
    Format response
    :param endpoint: endpoint details
    :param response: response from endpoint call
    :return: HttpResponse
    """
    try:
        data = json.loads(response.text)
    except JSONDecodeError:
        data = response.text
    return HttpResponse(env=endpoint.env,
                        url=endpoint.uri,
                        status=response.status_code,
                        headers=response.headers,
                        data=data,
                        content=response.content,
                        transaction-id=response.headers.get(transaction-id, NO_VALUE)
                        )


def send_request(endpoint: EndPoint) -> HttpResponse:
    """
    Factory method to call relevant method
    :param endpoint: endpoint details
    :param method: http method
    :return: HttpResponse
    """
    _module_functions = {name: obj for name, obj in inspect.getmembers(sys.modules[__name__])
                         if inspect.isfunction(obj)}
    return _module_functions[endpoint.method](endpoint)
