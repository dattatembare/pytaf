from typing import NamedTuple, Any

transaction_id = 'x-txid'
NO_VALUE = ''


class EndPoint(NamedTuple):
    uri: str
    method: str
    env: str
    headers: dict = {}
    params: dict = {}
    data: Any = {}
    json: Any = {}
    files: Any = {}


class HttpResponse(NamedTuple):
    env: str
    url: str
    status: str
    headers: Any
    data: Any = NO_VALUE
    content: bytes = b''
    error: Any = NO_VALUE
    transaction_id: str = NO_VALUE
