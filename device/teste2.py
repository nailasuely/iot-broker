import logging
import threading
import socket
import json
import time
import random
from datetime import datetime

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s - %(message)s')

class VirtualSensor:
    def __init__(self, server_host, server_port, broker_host, broker_port, sensor_name):
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
        self.is_on = False  # Iniciar o sensor desligado
        self.is_running = True  # Controle da thread
        self.register_with_broker()

    def send_data_to_broker(self, data):
        timeNow = str(datetime.now())[:19]
        message = {"source": self.sensor_name, "data": data, "time": timeNow, "type": self.sensor_type, 
                   "state": "on" if self.is_on else "off"}
        try:
            self.sock_data.sendto(json.dumps(message).encode(), (self.broker_host, self.broker_port))
            #logging.info(f"Sensor '{self.sensor_name}' sent data to broker: {data}")
        except Exception as e:
            logging.error(f"Error sending data to broker: {e}")

    def generate_data(self):
        if self.is_on:
            if self.sensor_type == "Temperature":
                data_value = round(random.uniform(self.min_value, self.max_value), 2)
                return f"{data_value}"
        return ""

    def change_sensor_name(self, new_name):
        old_name = self.sensor_name
        self.sensor_name = new_name
        logging.info(f"Sensor name changed from '{old_name}' to '{new_name}'")
        # Enviar mensagem ao broker informando a mudança de nome
        change_name_message = {"type": "change_name", "old_name": old_name, "new_name": new_name}
        self.sock_cmd.send(json.dumps(change_name_message).encode())

    def start(self):
        while self.is_running:
            if not self.is_on:
                break

            try:
                logging.info("Sensor data generation started")
                while self.is_running:
                    data = self.generate_data()
                    if data:
                        self.send_data_to_broker(data)
                    time.sleep(self.data_generation_interval)
            except KeyboardInterrupt:
                logging.info("Stopping sensor data generation...")
                self.is_running = False
                self.sock_data.close()
                self.sock_cmd.close()
                break

    def register_with_broker(self):
        while True:
            try:
                self.sock_cmd.connect((self.server_host, self.server_port))
                registration_message = {"type": "register", "name": self.sensor_name}
                self.sock_cmd.send(json.dumps(registration_message).encode())
                logging.info(f"Sensor '{self.sensor_name}' registered with broker")
                threading.Thread(target=self.receive_commands).start()
                self.is_on = True
                break
            except Exception as e:
                print("Trying to connect to the broker...\n")
                #logging.error(f"Error registering with broker: {e}")
                time.sleep(5)

    def receive_commands(self):
        try:
            logging.info(f"Receiving commands for sensor '{self.sensor_name}' started")
            while self.is_running:
                command = self.sock_cmd.recv(1024).decode()
                if not command:
                    print("Empty command received from broker")
                    break
                logging.info(f"Command received by sensor '{self.sensor_name}': {command}")
                self.process_command(command)
        except Exception as e:
            logging.error(f"Error receiving commands: {e}")
        finally:
            logging.info(f"Receiving commands for sensor '{self.sensor_name}' stopped")
            self.sock_cmd.close()  # Fechar o socket ao encerrar

    def process_command(self, command):
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
                logging.error("Invalid change_name command format. Usage: change_name <new_name>")
        else:
            logging.error("Invalid command")

    def turn_on(self):
        self.is_on = True
        logging.info("Sensor turned on")

    def turn_off(self):
        self.is_on = False
        logging.info("Sensor turned off")

    def restart(self):
        self.turn_off()
        time.sleep(1)
        self.turn_on()
        logging.info("Sensor restarted")

    def shutdown(self):
        try:
            # Enviar mensagem de desligamento para o broker
            shutdown_message = {"type": "shutdown", "name": self.sensor_name}
            self.sock_cmd.send(json.dumps(shutdown_message).encode())
            logging.info(f"Sent shutdown message to broker for sensor '{self.sensor_name}'")
        except Exception as e:
            logging.error(f"Error sending shutdown message to broker: {e}")

        # Encerrar a thread de recebimento de comandos
        self.is_running = False

        # Fechar os sockets
        self.sock_data.close()
        self.sock_cmd.close()

    
def menu(sensor):
    print("\nMenu:")
    print("1. Ligar o sensor")
    print("2. Desligar o sensor")
    print("3. Trocar o nome do sensor")
    print("4. Trocar o intervalo de geração de dados")
    print("5. Sair")

    while True:
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
            break
        elif choice == "5":
            logging.info("Saindo...")
            sensor.shutdown()  # Encerrar completamente o sensor
            return  # Encerrar a execução do menu
        else:
            print("Opção inválida. Tente novamente.")

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