import logging
import socket
import json
import threading
from flask import Flask, request, jsonify
from flask_cors import CORS
import time

#192.168.0.181

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s - %(message)s')

class Broker:
    """
    Essa é a classe responsável por gerenciar conexões de dispositivos e comandos.
    
    Esta classe inicializa um servidor para receber dados e comandos de dispositivos, 
    mantém registro dos dispositivos conectados e gerencia o envio de comandos para os dispositivosq eue estão
    conectados atualmente no sistema. 
    """

    def __init__(self, data_port, command_port):
        """
        Para inicializar o broker é necessário a porta de dados e a porta específica para comandos.

        Args:
            data_port (int): Porta para receber os dados do dispositivo.
            command_port (int): Porta para receber os comandos da aplicação.
        """
        self.ipHost = '0.0.0.0'
        self.data_port = data_port
        self.command_port = command_port
        self.devices = {}
        self.datas = {}
        self.last_operation = None
        self.lock = threading.Lock()
        self.setup_data_server()
        self.setup_command_server()
        self.ip = '0.0.0.0'

    def setup_data_server(self):
        """
        Configura o servidor de dados para receber dados dos dispositivos.
        """
        self.data_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.data_sock.bind((self.ipHost, self.data_port))
        logging.info(f"Ouvindo os dados recebidos de {self.ipHost}:{self.data_port}")
        self.start_escutarDados()

    def setup_command_server(self):
        """
        Configura o servidor de comandos para receber outros tipos de mensagens, como por exemplo
        o registro.
        """
        self.command_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.command_socket.bind((self.ipHost, self.command_port))
        self.command_socket.listen(6)
        logging.info(f"Ouvindo os comandos recebidos de {self.ipHost}:{self.command_port}")

    def start_escutarDados(self):
        """
        Para escutar os dados recebidos dos dispostivos é necessário uma thread específica para não 
        interromper as outras funções realizadas pelo broker. .
        """
        threading.Thread(target=self.processData).start()

    def update_last_operation(self, operation_type, device_name=None):
        """
        Essa função é apenas para guardar qual foi o ultimo comando feito.

        Args:
            operation_type (str): Tipo de operação realizada.
            device_name (str): Nome do dispositivo (não é sempre que precisa).
        """
        self.last_operation = {"type": operation_type, "device_name": device_name}
    
    def get_last_operation(self):
        """
        Função para obter o ultimo comando realizado. 

        Returns:
            dict: Última operação realizada.
        """
        return self.last_operation

    def processData(self):
        """
        Função feita para processar os dados recbidos do dispositivo, para isso ele decodifica usando 
        métodos UDP e Os dados recebidos são decodificados usando JSON.
        Json.loads é usado para decodificar os dados recebidos e posteriormente armazenados no dict de dados. 
        """
        while True:
            data, sender_address = self.data_sock.recvfrom(1024)
            message = json.loads(data.decode())
            logging.info(f"Dados recebidos do dispositivo: '{message['source']}': {message['data']}")
            self.datas[message['source']] = message
            with self.lock:
                for connection in self.datas.values():
                    if isinstance(connection, socket.socket):
                        try:
                            connection.send(json.dumps(message).encode())
                        except Exception as e:
                            logging.error(f"Erro para enviar dados para aplicação: {e}")
                            

    def manageDeviceConnection(self, connection, sender_address):
        """
        Feito para gerenciar as conexões com o dispositivo, sendo responsável por 
        gerenciar as conexões com os dispositivos conectados ao broker 

        Args:
            connection (socket.socket): Socket de conexão com o dispositivo.
            sender_address (tuple): Endereço do dispositivo.
        """
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
                    elif message["type"] == "notification":
                        action = message["action"]
                        device_name = message["name"]
                        logging.info(f"Recebida notificação do dispositivo '{device_name}': {action}")
                        self.update_last_operation(action, device_name)
                    else:
                        logging.error("Mensagem inválida recebida pela aplicação")
                except Exception as e:
                    logging.error(f"Erro para gerenciar com a conexão da aplicação: {e}")
                    break

    def register_device(self, name, connection):
        """
        Registra a conexão de um dispositivo na lista de dispostivios.

        Args:
            name (str): Nome do dispositivo.
            connection (socket.socket): Socket de conexão com o dispositivo.
        """
        with self.lock:
            self.devices[name] = connection
            logging.info(f"Device '{name}' registrado")

    def shutdown_device(self, device_name):
        """
        Desconecta um dispositivo da lista de dispostivos. 

        Args:
            device_name (str): Nome do dispositivo.
        """
        with self.lock:
            if device_name in self.devices:
                del self.devices[device_name]
                logging.info(f"Device '{device_name}' removido do dicionário do broker")
            else:
                logging.error(f"Device '{device_name}' não encontrado no dicionário do broker")

    def send_change_name_command(self, device_name, new_name):
        """
        Envia um comando para alterar o nome de um dispositivo.

        Args:
            device_name (str): Nome atual do dispositivo.
            new_name (str): Novo nome do dispositivo.
        """
        command = f"change_name {new_name}"
        self.send_command_to_device(device_name, command)
        self.change_device_name(device_name, new_name) 
        
    def change_device_name(self, antigo_name, new_name):
        """
        Funçao para alterar o nome de um dispostivo. 

        Args:
            antigo_name (str): Nome atual do dispositivo.
            new_name (str): Novo nome do dispositivo.
        """
        with self.lock:
            if antigo_name in self.devices:
                self.devices[new_name] = self.devices.pop(antigo_name)
                logging.info(f"Device name changed from '{antigo_name}' to '{new_name}'")
            else:
                logging.error(f"Device '{antigo_name}' não encontrado")

    def send_command_to_device(self, device_name, command):
        """
        Função apra enviar o comando para o dispotivo, como por exemplo o comando de ligar.

        Args:
            device_name (str): Nome do dispositivo.
            command (str): Comando a ser enviado.
        """
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

    def remove_inactive_devices(self, timeout=10, grace_period=5):
        """
        Remove dispositivos inativos que não enviaram dados por um tempo especificado.

        Args:
            timeout (int): Tempo limite em segundos para considerar um dispositivo inativo.
            grace_period (int): Período de tolerância após o tempo limite antes de remover o dispositivo.
        """
        while True:
            current_time = time.time()
            inactive_devices = []
            with self.lock:
                for device_name, data in self.datas.items():
                    last_data_time = data.get("time", 0)
                
                    if current_time - last_data_time > timeout:
                        
                        if device_name in self.devices:
                          
                            inactive_devices.append(device_name)
                        else:
                            
                            self.shutdown_device(device_name)
                            logging.info(f"Device '{device_name}' removido da lista de dispositivos devido à inatividade")

           
            for device_name in inactive_devices:
                last_data_time = self.datas[device_name].get("time", 0)
                if current_time - last_data_time > timeout + grace_period:
                    self.shutdown_device(device_name)
                    logging.info(f"Device '{device_name}' removido da lista de dispositivos devido à inatividade")
            time.sleep(timeout / 2)  
                
    def start(self):
        """
        Inicia o servidor para gerenciar conexões com os dispositivos, tudo isso através de uma thread específica. 
        """
        while True:
            connection, sender_address = self.command_socket.accept()
            threading.Thread(target=self.manageDeviceConnection, args=(connection, sender_address)).start()

app = Flask(__name__)
CORS(app)
broker = Broker(9998, 9999)

@app.route('/devices', methods=['GET'])
def get_devices():
    """
    Rota para listar os dispositivos registrados.

    Returns:
        str: Lista de nomes de dispositivos registrados em formato JSON.
    """
    devices = list(broker.devices.keys())
    return json.dumps(devices)

@app.route('/devices/<device_name>/name', methods=['PUT'])
def change_device_name(device_name):
    """
    Rota para alterar o nome de um dispositivo.

    Args:
        device_name (str): Nome atual do dispositivo.

    Returns:
        str: Mensagem indicando o sucesso da operação ou um erro em formato JSON.
    """
    new_name = request.json.get('new_name')
    if new_name:
        if device_name in broker.devices:
            broker.send_change_name_command(device_name, new_name)
            return jsonify({'message': f'Device name changed to "{new_name}"'}), 200
        else:
            return jsonify({'error': f'Device "{device_name}" not registered'}), 404
    else:
        return jsonify({'error': 'New name not provided'}), 400
    

@app.route('/devices/<device_name>/data', methods=['GET'])
def get_device_data(device_name):
    """
    Rota para obter os dados de um dispositivo.

    Args:
        device_name (str): Nome do dispositivo.

    Returns:
        str: Dados do dispositivo em formato JSON ou uma mensagem de erro caso o dispositivo não seja encontrado.
    """
    data = broker.datas.get(device_name)
    return json.dumps({"data": data}) if data else json.dumps({"error": "Device not found"})

@app.route('/devices/<device_name>/command', methods=['POST'])
def send_command(device_name):
    """
    Rota para enviar um comando para um dispositivo.

    Args:
        device_name (str): Nome do dispositivo.

    Returns:
        str: Mensagem indicando o sucesso da operação ou um erro em formato JSON.
    """
    command = request.json.get('command')
    if command:
        if device_name in broker.devices:
            broker.send_command_to_device(device_name, command)
            broker.update_last_operation(command, device_name)
            return jsonify({'message': f'Command "{command}" sent to device "{device_name}"'}), 200
        else:
            return jsonify({'error': f'Device "{device_name}" not registered'}), 404
    else:
        return jsonify({'error': 'Command not provided'}), 400
    
@app.route('/last_command', methods=['GET'])
def get_last_command():
    """
    Rota para obter a última operação realizada.

    Returns:
        str: Última operação realizada em formato JSON ou uma mensagem de erro caso não haja operações.
    """
    last_command = broker.get_last_operation()
    if last_command:
        return jsonify({'last_command': last_command}), 200
    else:
        return jsonify({'error': 'Nenhum comando foi dado ainda'}), 404

if __name__ == "__main__":
    threading.Thread(target=broker.start).start()
    app.run(host=broker.ip, port=5001)
