import json

from lib.utils import get_basic_auth_key


def update_auth_key():
    with open('config/auth.json', 'w') as file:
        file.write(json.dumps({'Authorization': get_basic_auth_key()}))
    print('Authentication key updated successfully!')


"""
Command to update Authorization key:
    client=pytaf>update_auth.py
Enter username/password and you are all set.
"""
if __name__ == '__main__':
    update_auth_key()
