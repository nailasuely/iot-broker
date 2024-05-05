import logging
import threading
import socket
import json
import time
import random
from datetime import datetime
import os 

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s - %(message)s')

class VirtualSensor:
    """
    Essa classe é utilizada para ser o dispositivo que é um simulador de sensor. 
    Então, epresenta um sensor virtual que gera dados de temperatura e os envia para um broker.

    """

    def __init__(self, server_host, server_port, broker_host, broker_port, sensor_name):
        """
        Função que inicializa a classe. 

        Args:
            server_host (str): Endereço IP do servidor para registro.
            server_port (int): Porta do servidor para registro.
            broker_host (str): Endereço IP do broker.
            broker_port (int): Porta do broker.
            sensor_name (str): Nome do sensor.
        """
        self.server_host = server_host
        self.server_port = server_port
        self.broker_host = broker_host
        self.broker_port = broker_port 
        self.sensor_name = sensor_name
        self.sock_data = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock_cmd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.data_generation_interval = 1
        self.min_value = 0
        self.max_value = 50
        self.sensor_type = "Temperature"
        self.is_on = False
        self.is_running = True
        self.register_with_broker()

    def send_data_to_broker(self, data):
        """
        Aqui os dados são enviados em  UDP

        Args:
            data (str): Dados a serem enviados.
        """
        timeNow = str(datetime.now())[:19]
        message = {"source": self.sensor_name, "data": data, "time": timeNow, "type": self.sensor_type, 
                   "state": "on" if self.is_on else "off"}
        try:
            self.sock_data.sendto(json.dumps(message).encode(), (self.broker_host, self.broker_port))
        except Exception as e:
            logging.error(f"Erro ao enviar dados para o broker: {e}")

    def generate_data(self):
        """
        Aqui os dados são simulados para enviar para os clientes. 

        Returns:
            str: Dados de temperatura gerados.
        """
        if self.is_on:
            if self.sensor_type == "Temperature":
                data_value = round(random.uniform(self.min_value, self.max_value), 2)
                return f"{data_value}"
        return ""

    def change_sensor_name(self, new_name):
        """
        Função para alterar o nome do sensr. 

        Args:
            new_name (str): Novo nome do sensor.
        """
        old_name = self.sensor_name
        self.sensor_name = new_name
        logging.info(f"Nome do sensor alterado de '{old_name}' para '{new_name}'")
        change_name_message = {"type": "change_name", "old_name": old_name, "new_name": new_name}
        self.sock_cmd.send(json.dumps(change_name_message).encode())

    def start(self):
        """
        Inicia a o sensor e a geração de dados com uma série de validações. 
        """
        while self.is_running:
            if not self.is_on:
                break

            try:
                logging.info("Iniciando geração de dados do sensor")
                while self.is_running:
                    data = self.generate_data()
                    if data:
                        self.send_data_to_broker(data)
                    time.sleep(self.data_generation_interval)
            except KeyboardInterrupt:
                logging.info("Parando a geração de dados do sensor...")
                self.is_running = False
                self.sock_data.close()
                self.sock_cmd.close()
                break

    def register_with_broker(self):
        """
        Função para registrar o sensor no broker. 
        """
        while True:
            try:
                self.sock_cmd.connect((self.server_host, self.server_port))
                registration_message = {"type": "register", "name": self.sensor_name}
                self.sock_cmd.send(json.dumps(registration_message).encode())
                logging.info(f"Sensor '{self.sensor_name}' registrado com o broker")
                threading.Thread(target=self.receive_commands).start()
                self.is_on = True
                break
            except Exception as e:
                print("Tentando se conectar ao broker...\n")
                time.sleep(5)

    def receive_commands(self):
        """
        Recebe os comandos do broker via tcp. 
        """
        try:
            logging.info(f"Iniciando recebimento de comandos para o sensor '{self.sensor_name}'")
            while self.is_running:
                command = self.sock_cmd.recv(1024).decode()
                if not command:
                    print("Comando vazio recebido do broker")
                    break
                logging.info(f"Comando recebido pelo sensor '{self.sensor_name}': {command}")
                self.process_command(command)
        except Exception as e:
            logging.error(f"Erro ao receber comandos: {e}")
        finally:
            logging.info(f"Parando o recebimento de comandos para o sensor '{self.sensor_name}'")
            self.sock_cmd.close()

    def process_command(self, command):
        """
        Essa função foi feita para processar os comandos recebidos do broker. 

        Args:
            command (str): Comando recebido.
        """
        if command == "turn_on":
            self.turn_on()
        elif command == "turn_off":
            self.turn_off()
        elif command == "restart":
            self.restart()
        elif command == "get_temperature":
            data = self.generate_data()
            if data:
                self.send_data_to_broker(data)
        elif command.startswith("change_name"):  
            parts = command.split()
            if len(parts) == 2:
                new_name = parts[1]
                self.change_sensor_name(new_name)
            else:
                logging.error("Formato de comando change_name inválido. Uso: change_name <novo_nome>")
        else:
            logging.error("Comando inválido")

    def turn_on(self):
        """
        Função para ligar o sensor.
        """
        self.is_on = True
        logging.info("Sensor ligado")
        try:
            notification_message = {"type": "notification", "action": "turn_on", "name": self.sensor_name}
            self.sock_cmd.send(json.dumps(notification_message).encode())
            logging.info("Notificação de ligar enviada para o broker")
        except Exception as e:
            logging.error(f"Erro ao enviar notificação de ligar para o broker: {e}")
            
    def turn_off(self):
        """
        Função para desligar o sensor.
        """
        self.is_on = False
        logging.info("Sensor desligado")
        try:
            notification_message = {"type": "notification", "action": "turn_off", "name": self.sensor_name}
            self.sock_cmd.send(json.dumps(notification_message).encode())
            logging.info("Notificação de desligar enviada para o broker")
        except Exception as e:
            logging.error(f"Erro ao enviar notificação de desligar para o broker: {e}")

    def restart(self):
        """
        Função para reiniciar o sensor.
        """
        self.turn_off()
        time.sleep(1)
        self.turn_on()
        logging.info("Sensor reiniciado")
        try:
            notification_message = {"type": "notification", "action": "restart", "name": self.sensor_name}
            self.sock_cmd.send(json.dumps(notification_message).encode())
            logging.info("Notificação de reiniciar enviada para o broker")
        except Exception as e:
            logging.error(f"Erro ao enviar notificação de reiniciar para o broker: {e}")

    def shutdown(self):
        """
        Desliga completamente o sensor fechando todas as portas e envia o aviso para o broker que foi desligado. 
        """
        try:
            shutdown_message = {"type": "shutdown", "name": self.sensor_name}
            self.sock_cmd.send(json.dumps(shutdown_message).encode())
            logging.info(f"Mensagem de desligamento enviada para o broker para o sensor '{self.sensor_name}'")
        except Exception as e:
            logging.error(f"Erro ao enviar mensagem de desligamento para o broker: {e}")

        self.is_running = False

        self.sock_data.close()
        self.sock_cmd.close()

def clear_terminal():
    """
    Limpa o terminal.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def menu(sensor):
    """
    Menuzinho para controlar o sensor

    Args:
        sensor (VirtualSensor): Instância do sensor virtual.
    """
    while True:
        clear_terminal()
        print("─────────────────────────────────────────────────")
        print("\nBem vindo ao menu:")
        print("1. Ligar o sensor")
        print("2. Desligar o sensor")
        print("3. Trocar o nome do sensor")
        print("4. Trocar o intervalo de geração de dados")
        print("5. Sair")
        print("─────────────────────────────────────────────────\n")

        choice = input("Escolha uma opção: ")
        if choice == "1":
            sensor.turn_on()  
        elif choice == "2":
            sensor.turn_off()
        elif choice == "3":
            new_name = input("Digite o novo nome para o sensor: ")
            sensor.change_sensor_name(new_name)
        elif choice == "4":
            new_interval = int(input("Digite o novo intervalo (em segundos) para geração de dados: "))
            sensor.data_generation_interval = new_interval
        elif choice == "5":
            logging.info("Saindo...")
            sensor.shutdown()
            return
        else:
            print("Opção inválida. Tente novamente.")
        input("Pressione Enter para continuar...")

if __name__ == "__main__":
    server_ip = input("IP do servidor para se registrar: ")
    data_server_port = 9999
    broker_port = 9998
    sensor_name = "TemperatureSensor"

    sensor = VirtualSensor(server_ip, data_server_port, server_ip, broker_port, sensor_name)

    sensor_thread = threading.Thread(target=sensor.start)
    sensor_thread.start()

    menu(sensor)

    sensor_thread.join()

    logging.info("Programa encerrado completamente.")
