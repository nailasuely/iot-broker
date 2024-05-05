import logging
import socket
import json
import threading
from flask import Flask, request, jsonify
from flask_cors import CORS

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s - %(message)s')

#192.168.0.181
#/home/tec502/Downloads/iot-broker-main/broker
class Broker:
    def __init__(self, data_port, command_port):
        self.ipHost = '0.0.0.0'
        # porta para receber os dados do dispostivo 
        self.data_port = data_port 
        # aqui a porta para
        self.command_port = command_port
        self.devices = {}
        self.datas = {}
        self.last_operation = None
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

    def update_last_operation(self, operation_type, device_name=None):
        self.last_operation = {"type": operation_type, "device_name": device_name}
    
    def get_last_operation(self):
        return self.last_operation

    def processData(self):
        while True:
            data, sender_address = self.data_sock.recvfrom(1024)
            message = json.loads(data.decode())
            logging.info(f"Dados recebidos do dispositivo: '{message['source']}': {message['data']}")
            self.datas[message['source']] = message
            #o envio dos dados recebidos para todas as conexões com a aplicação
            with self.lock:
                for connection in self.datas.values():
                    if isinstance(connection, socket.socket):
                        try:
                            connection.send(json.dumps(message).encode())
                        except Exception as e:
                            logging.error(f"Erro para enviar dados para aplicação: {e}")
                            

    def manageDeviceConnection(self, connection, sender_address):
        with connection:
            logging.info(f"Nova conexão com: {sender_address}")
            while True:
                try:
                    data = connection.recv(1024).decode()
                    if not data:
                        logging.info(f"Conexão fechada com: {sender_address}")
                        with self.lock:
                            for name, connectionection in list(self.devices.items()):
                                if connectionection == connection:
                                    del self.devices[name]
                                    logging.info(f"Dispositivo '{name}' desconectado")
                        break
                    message = json.loads(data)
                    if message["type"] == "register":
                        device_name = message["name"]
                        self.register_device(device_name, connection)
                        self.update_last_operation("register", device_name)
                    elif message["type"] == "command":
                        device_name = message["device"]
                        command = message["command"]
                        print("\n\n\n\ opa opa opa")
                        self.update_last_operation(command, device_name)
                        self.send_command_to_device(device_name, command)
                        
                    elif message["type"] == "shutdown":
                        device_name = message["name"]
                        self.shutdown_device(device_name)
                        self.update_last_operation("shutdown", device_name)
                    elif message["type"] == "change_name":
                        old_name = message["old_name"]
                        new_name = message["new_name"]
                        self.change_device_name(old_name, new_name)
                        self.update_last_operation("change_name", new_name)
                    else:
                        logging.error("Mensagem inválida recebida pela aplicação")
                except Exception as e:
                    logging.error(f"Erro para gerenciar com a conexão da aplicação: {e}")
                    break


    def register_device(self, name, connection):
        with self.lock:
            self.devices[name] = connection
            logging.info(f"Device '{name}' registered")

    def shutdown_device(self, device_name):
        with self.lock:
            if device_name in self.devices:
                del self.devices[device_name]
                logging.info(f"Device '{device_name}' removido do dicionário do broker")
            else:
                logging.error(f"Device '{device_name}' não encontrado no dicionário do broker")

    def send_change_name_command(self, device_name, new_name):
        command = f"change_name {new_name}"
        self.send_command_to_device(device_name, command)
        self.change_device_name(device_name, new_name) 
        
    def change_device_name(self, antigo_name, new_name):
        with self.lock:
            if antigo_name in self.devices:
                self.devices[new_name] = self.devices.pop(antigo_name)
                logging.info(f"Device name changed from '{antigo_name}' to '{new_name}'")
            else:
                logging.error(f"Device '{antigo_name}' not found")

    def send_command_to_device(self, device_name, command):
        with self.lock:
            if device_name in self.devices:
                try:
                    connection = self.devices[device_name]
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
    return json.dumps(devices)

@app.route('/devices/<device_name>/name', methods=['PUT'])
def change_device_name(device_name):
    new_name = request.json.get('new_name')
    if new_name:
        if device_name in broker.devices:
            broker.send_change_name_command(device_name, new_name)
            return jsonify({'message': f'Device name changed to "{new_name}"'}), 200
        else:
            return jsonify({'error': f'Device "{device_name}" not registered'}), 404
    else:
        return jsonify({'error': 'New name not provided'}), 400
    

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
            broker.update_last_operation(command, device_name)
            return jsonify({'message': f'Command "{command}" sent to device "{device_name}"'}), 200
        else:
            return jsonify({'error': f'Device "{device_name}" not registered'}), 404
    else:
        return jsonify({'error': 'C5mand not provided'}), 400
    
@app.route('/last_command', methods=['GET'])
def get_last_command():
    last_command = broker.get_last_operation()
    if last_command:
        return jsonify({'last_command': last_command}), 200
    else:
        return jsonify({'error': 'Nenhum comando foi dado ainda'}), 404

if __name__ == "__main__":
    threading.Thread(target=broker.start).start()
    app.run(host=broker.ip, port=5001)