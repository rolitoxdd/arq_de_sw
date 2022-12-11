import socket
from services.utils import str_bus_format, w_print, f_print, g_print, h_print, b_print, bcolors

# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_address = ('localhost', 5000)
# sock.connect(server_address)


class App:
    def __init__(self, login_service, services=[]) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 5000)
        self.sock.connect(server_address)
        self.services = services
        self.login_service = login_service

    def send_message(self, data, service_name='g7999'):
        req = str_bus_format(data, service_name).encode('UTF-8')
        self.sock.send(req)
        return self.sock.recv(4096).decode('UTF-8')

    def login(self):
        h_print('\n', '-'*20, 'Login', '-'*20, '\n')
        inputs = {}
        for i in range(len(self.login_service['inputs'])):
            actual_input = self.login_service['inputs'][i]
            key = actual_input['key']
            inputs[key] = input(actual_input['desc'])
        res = self.send_message(inputs, self.login_service['id'])
        return res

    def show_menu(self):
        while True:
            h_print("\n", "-"*20, "Bienvenido", "-"*20, "\n")
            b_print("Menu de opciones:\n")
            print("Opcion 1: {}".format(self.login_service['desc']))
            print("Opcion 0: Salir")
            option = input('Ingrese una opcion: ')
            if option == '1':
                res = self.login()
                data = eval(res[12:])
                if res[10:12] == 'NK':
                    f_print('Servicio no disponible')
                    pass
                elif data == None:
                    f_print('Login fallido')
                    pass
                else:
                    g_print('Login exitoso')
                    break
            elif option == '0':
                return
            else:
                w_print("Opcion no valida")
        self.menu(data[-1])

    def menu(self, type_id):
        while True:
            input(
                f'{bcolors.UNDERLINE}Presione enter para continuar...{bcolors.ENDC}')
            h_print("\n", "-"*20, "Bienvenido", "-"*20, "\n")
            b_print("Menu de opciones:\n")
            available_services = [
                service for service in self.services if type_id in service['user_types']
            ]
            services = {}
            for i in range(len(available_services)):
                actual_service = available_services[i]
                services[f'{i+1}'] = actual_service
                print("Opcion {}: {}".format(i+1, actual_service['desc']))
            print("Opcion 0: Salir")
            option = input('Ingrese una opcion: ')
            if option == '0':
                return
            elif option in services:
                service = services[option]
                inputs = {}
                for i in range(len(service['inputs'])):
                    actual_input = service['inputs'][i]
                    key = actual_input['key']
                    inputs[key] = input(actual_input['desc'])
                res = self.send_message(inputs, service['id'])
                if res[10:12] == 'NK':
                    f_print('Servicio no disponible')
                    pass
                else:
                    service['function'](res)
            else:
                w_print("Opcion no valida")


def display_maquinarias(res):
    data = eval(res[12:])
    g_print('Maquinarias encontradas:')
    for maquinaria in data:
        b_print('-'*20)
        print('id', maquinaria[0])
        print('nombre', maquinaria[1])
        print('estado', maquinaria[2])
        print('costo', maquinaria[3])
        print('fecha de creacion', maquinaria[4])


if __name__ == '__main__':
    app = App(
        login_service={
            'id': 'serv1',
            'desc': 'Iniciar sesión',
            'inputs': [
                {
                    'key': 'username',
                    'desc': 'Ingresa tu rut: '
                },
                {
                    'key': 'password',
                    'desc': 'Ingresa tu contraseña: '
                }
            ]
        },
        services=[
            {
                'id': 'serv2',
                'desc': 'Registrar maquinaria',
                'user_types': [0, 1, 2],
                'function': lambda *_: g_print('maquinaria registrada'),
                'inputs': [
                    {
                        'key': 'nombre',
                        'desc': 'Ingresa el nombre de la maquinaria: ',
                    },
                    {
                        'key': 'estado',
                        'desc': 'Ingresa el estado de la maquinaria: ',
                    },
                    {
                        'key': 'costo',
                        'desc': 'Ingresa el costo de la maquinaria: '
                    }
                ]
            },
            {
                'id': 'serv3',
                'desc': 'Consultar maquinarias',
                'user_types': [0, 1, 2],
                'function': display_maquinarias,
                'inputs': [
                    {
                        'key': 'id',
                        'desc': 'Ingresa el id de la maquinaria o vacío para consultar por todas: '
                    }
                ]
            },
            {
                'id': 'serv4',
                'desc': 'Modificar maquinaria',
                'user_types': [0, 1, 2],
                'function': lambda res: g_print('maquinaria modificada') if len(eval(res[12:])) > 0 else f_print('maquinaria no encontrada'),
                'inputs': [
                    {
                        'key': 'id',
                        'desc': 'Ingresa el id de la maquinaria: '
                    },
                    {
                        'key': 'nombre',
                        'desc': 'Ingresa el nuevo nombre de la maquinaria: ',
                    },
                    {
                        'key': 'estado',
                        'desc': 'Ingresa el nuevo estado de la maquinaria: ',
                    },
                    {
                        'key': 'costo',
                        'desc': 'Ingresa el nuevo costo de la maquinaria: '
                    }
                ]
            }
        ])
    res = app.show_menu()
