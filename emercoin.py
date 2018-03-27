import json

import requests


class EmercoinClient(object):
    def __init__(self,
               user='emccoinrpc',
               password='secret_password',
               protocol='http',
               host='127.0.0.1',
               port=6662):
        self.allowed_methods = ['name_new', 'name_show', 'name_mempool', 'name_update', 'name_list']

        self.user = user
        self.password = password
        self.protocol = protocol
        self.host = host
        self.port = port

    def call_command(self, command, *args):

        credentials = f"{self.user}:{self.password}@"
        url = f"{self.protocol}://{credentials}{self.host}:{self.port}"

        data = {'method': command}

        if args:
            data['params'] = args
        try:
            response = requests.post(url=url, data=json.dumps(data))
            data = response.json()
        except requests.ConnectionError:
            return {'result': None, 'error':{'code': 999999, 'message': "can't connect server"}}
        except ValueError:
            error_msg = "can't connect server"
            if response.status_code == 401:
                error_msg = 'unauthorized'
            return {'result': None, 'error':{'code': 999999, 'message': error_msg}}
        return data

    def name_new(self):
        name = input('name ')
        value = input('value ')
        days = int(input('days '))
        return self.call_command('name_new', name, value, days)

    def name_update(self):
        name = input('name ')
        value = input('value ')
        days = int(input('days '))
        return self.call_command('name_update', name, value, days)

    def name_show(self):
        name = input('name ')
        return self.call_command('name_show', name)

    def name_list(self):
        return self.call_command('name_list')

    def name_mempool(self):
        return self.call_command('name_mempool')


if __name__ == '__main__':
    client = EmercoinClient()
    print('Hi! Im simple emercoin client')
    while True:
        print('You can use methods:')
        print(*client.allowed_methods)
        print()
        command = input('input method name ')
        if command not in client.allowed_methods:
            print('please use allowed methods')
            print(*client.allowed_methods)
            print()
        elif command == 'name_new':
            result = client.name_new()
            print(result)
        elif command == 'name_update':
            result = client.name_update()
            print(result)
        elif command == 'name_show':
            result = client.name_show()
            print(result)
        elif command == 'name_list':
            result = client.name_list()
            print(result)
        elif command == 'name_mempool':
            result = client.name_mempool()
            print(result)
