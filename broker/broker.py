import logging
import socket
import json
import threading
from flask import Flask, request, jsonify
from flask_cors import CORS

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s - %(message)s')

class Broker:
    def __init__(self, data_port, command_port):
        self.ipHost = '0.0.0.0'
        # porta para receber os dados do dispostivo 
        self.data_port = data_port 
        # aqui a porta para
        self.command_port = command_port
        self.devices = {}
        self.datas = {}
        # coisa p ajudar o acesso compartilhado em vários recursos compartilhados pelas threads
        # estava tendo um errinho nessa parte, resolver depois + 
        self.lock = threading.Lock()
        self.setup_data_server()
        self.setup_command_server()
        self.ip = '0.0.0.0'

    # feito com socket udp para dados que é a abordagem não confiável falada no texto do problema
    def setup_data_server(self):
        self.data_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.data_sock.bind((self.ipHost, self.data_port))
        logging.info(f"Ouvindo os dados recebidos de {self.ipHost}:{self.data_port}")
        # aqui para iniciar e começar a ouvir os dados enviados pelo dispositivo
        self.start_escutarDados()

    # feito com socket tcp para comandos 
    def setup_command_server(self):
        self.command_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.command_socket.bind((self.ipHost, self.command_port))
        # escuta os comandos das aplicações, permitindo até 6 na fila 
        self.command_socket.listen(6)
        logging.info(f"Ouvindo os comandos recebidos de {self.ipHost}:{self.command_port}")

    def start_escutarDados(self):
        threading.Thread(target=self.processData).start()

    def processData(self):
        while True:
            data, sender_address = self.data_sock.recvfrom(1024)
            message = json.loads(data.decode())
            logging.info(f"Dados recebidos do dispositivo: '{message['source']}': {message['data']}")
            self.datas[message['source']] = message['data']
            #o envio dos dados recebidos para todas as conexões com a aplicação
            with self.lock:
                for connection in self.datas.values():
                    if isinstance(connection, socket.socket):
                        try:
                            connection.send(json.dumps(message).encode())
                        except Exception as e:
                            logging.error(f"Erro para enviar dados para aplicação: {e}")
                            

    def manageDeviceConnection(self, connection, sender_address):
        # oq eu usei para entender como usar conexões/bloco de contexo: 
        # https://docs.kanaries.net/pt/topics/Python/context-manager-python
        with connection:
            logging.info(f"Nova conexão com: {sender_address}")
            while True:
                try:
                    data = connection.recv(1024).decode()
                    if not data:
                        logging.info(f"Conexão fechada com: {sender_address}")
                        # Remove o dispositivo da lista quando a conexão é fechada
                        with self.lock:
                            for name, connectionection in list(self.devices.items()):
                                if connectionection == connection:
                                    del self.devices[name]
                                    logging.info(f"Dipositivo '{name}' desconectado")
                        break
                    message = json.loads(data)
                    if message["type"] == "register":
                        self.register_device(message["name"], connection)
                    elif message["type"] == "command":
                        device_name = message["device"]
                        command = message["command"]
                        self.send_command_to_device(device_name, command)
                    else:
                        logging.error("Mensagem inválida recebida pela aplicação")
                except Exception as e:
                    logging.error(f"Erro para gerenciar com a conexão da aplicação: {e}")
                    break


    def register_device(self, name, connection):
        with self.lock:
            self.devices[name] = connection
            print("\n\n\n o registro", connection, "\n\n\n")
            logging.info(f"Device '{name}' registered")

    def send_command_to_device(self, device_name, command):
        with self.lock:
            if device_name in self.devices:
                try:
                    connection = self.devices[device_name]
                    print("\n\n\n", connection, "\n\n\n")
                    connection.send(command.encode())
                    logging.info(f"Comando '{command}' enviado para o dispositivo: '{device_name}'")
                except Exception as e:
                    logging.error(f"Erro para enviar o comando para o dispositivo '{device_name}': {e}")
            else:
                logging.error(f"Device '{device_name}' não registrado")
                
    def start(self):
        while True:
            connection, sender_address = self.command_socket.accept()
            threading.Thread(target=self.manageDeviceConnection, args=(connection, sender_address)).start()

app = Flask(__name__)
CORS(app)
broker = Broker(9998, 9999)


# ROTAS HTTP 
@app.route('/devices', methods=['GET'])  # Rota para listar os dispositivos
def get_devices():
    devices = list(broker.devices.keys())
    print(devices)
    return json.dumps(devices)

# Rota para obter dados do dispositivo
@app.route('/devices/<device_name>/data', methods=['GET']) 
def get_device_data(device_name):
    data = broker.datas.get(device_name)
    return json.dumps({"data": data}) if data else json.dumps({"error": "Device not found"})

# Rota para enviar comandos para o dispositivo
@app.route('/devices/<device_name>/command', methods=['POST'])  
def send_command(device_name):
    command = request.json.get('command')
    if command:
        # se o dispositivo não estiver registrado, não passa daqui 
        if device_name in broker.devices:  
            broker.send_command_to_device(device_name, command)
            return jsonify({'message': f'Command "{command}" sent to device "{device_name}"'})
        else:
            return jsonify({'error': f'Device "{device_name}" not registered'}), 404
    else:
        return jsonify({'error': 'Command not provided'}), 400

if __name__ == "__main__":
    threading.Thread(target=broker.start).start()
    app.run(host=broker.ip, port=5001)