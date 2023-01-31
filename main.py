# borku
import csv
import os


CLIENT_TABLE = '.clients.csv'
CLIENT_SCHEMA = ['name', 'company', 'email', 'position'] # list of the keys the dictionary
clients = []


def _initialize_clients_from_storage():
    # used at the beginning of program execution
    with open(CLIENT_TABLE, mode = 'r') as f:
        reader = csv.DictReader(f, fieldnames = CLIENT_SCHEMA)
        for row in reader: 
            clients.append(row) # the row is the representation of each client how if was a dictionary 


def _save_clients_to_storage():
    # is used at the end of program execution
    tmp_table_name = '{}.tmp'.format(CLIENT_SCHEMA) # temporary table
    with open(tmp_table_name, mode = 'w') as f:
        writer = csv.DictWriter(f, fieldnames = CLIENT_SCHEMA)
        writer.writerows(clients)
        os.remove(CLIENT_TABLE)
        os.rename(tmp_table_name, '.clients.csv')


def _welcome():
    print('Welcome to Borku')
    print('What would you like today?')
    print('*'*26)
    print('[C]: create client')
    print('[l]: list clients')
    print('[U]: update client')
    print('[D]: delete client')
    print('[S]: search client')


def create_client(client):
    global clients
    if client not in clients:
        clients.append(client)
    else:
        print('Client already exists')
    

def list_clients():
    print('  uid  |  name  |  company  |  email  |  position  ')
    print('*' * 50)

    for idx, client in enumerate(clients):
        print('{cid} | {name} | {company} | {email} | {position}'.format(
            cid=idx, 
            name=client['name'], 
            company=client['company'], 
            email=client['email'], 
            position=client['position']))


def update_client(client_id):
    global clients
    if client_id <= len(clients) -1:
        print('Update client data')
        clients[client_id] = _client_data()
    else:
        _client_not_found(client_id)


def delete_client(client_id):
    global clients
    if client_id <= len(clients) -1:
        del clients[client_id]
        print(f'The client {client_id} was deleted')
    else:
        _client_not_found(client_id)
    return clients
    

def search_client(client_name):
    global clients
    for client_id, client_data in enumerate(clients):
        if client_data['name'] == client_name:
            print(f'The client/s "{client_name}" is in list.\nYour client id is: {client_id}')
    if client_data['name'] != client_name:
        _client_not_found(client_name)
    return clients


def _client_not_found(client_name):
	return print(f'The client "{client_name}" is not in clients list')


def _client_data():
    client = {
        'name': _get_client_field('name'),
        'company': _get_client_field('company'),
        'email': _get_client_field('email'),
        'position': _get_client_field('position'),
    }
    return client


def _get_client_field(field_name):
    field = None
    while not field:
        field = input(f'What is client {field_name}? ')
    return field


def _validate_client_id():
    while True: 
        try:
            client_id = int(_get_client_field('id'))
            break
        except ValueError:
            print('Input a client id number valid.')
    return client_id


def _input_command():
    commands = 'c,l,u,d,s'
    command = input('Input command: ').lower()
    while command not in commands or command == '':
        print('Invalid command. Try again.')
        command = input('Input command: ').lower()
    return command


def run(command):
    if command == 'c':
        client = _client_data()
        create_client(client)
    elif command == 'l':
        list_clients()
    elif command == 'u':
        client_id =_validate_client_id()
        update_client(client_id)
    elif command == 'd':
        client_id =_validate_client_id()
        delete_client(client_id)
    elif command == 's':
        client_name = _get_client_field('name')
        search_client(client_name)


def _start_again():
    return input('Exit? \n[Y]: yes\n[N]: no\nInput command: ').lower()


if __name__ == '__main__':
    _initialize_clients_from_storage()
    start_again = True
    while start_again:
        _welcome()
        command = _input_command()
        run(command)
        print('')
        start_again = _start_again()
        print('')
        if start_again == 'y':
            start_again = False
        elif start_again == 'n':
            start_again = True
        elif start_again != 'y' and start_again != 'n':
            while start_again != 'y' and start_again != 'n':
                print('Invalid command. Try again.')
                start_again = _start_again()
                print('')
            if start_again == 'y':
                start_again = False
            elif start_again == 'n':
                start_again = True
                
    print('The program has finished')
    
    _save_clients_to_storage()
    