import socket
from services.utils import str_bus_format, w_print, f_print, g_print, h_print, b_print

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

        print('En este punto debería mostrar el menu de servicios')


if __name__ == '__main__':
    app = App(
        login_service={
            'id': 'serv1',
            'desc': 'Iniciar sesión',
            'inputs': [{'key': 'username', 'desc': 'Ingresa tu rut: '}, {'key': 'password', 'desc': 'Ingresa tu contraseña: '}]
        },
        services=[
            {
                'id': 'serv2',
                'desc': 'Mandar un mensaje',
                'inputs': [{'key': ' mensaje: '}]
            }
        ])
    res = app.show_menu()
