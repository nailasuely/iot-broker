import logging
import threading
import socket
import json
import time
import random
import ipaddress
from datetime import datetime

# comandos p eu nao esquecer
# docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' fab528579903
# cat broker.log


# como usar o logging: https://docs.python.org/3/library/logging.html
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
        self.is_on = True
        self.register_with_broker()

    def send_data_to_broker(self, data):
        timeNow =  str(datetime.now())[0:19]
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
        self.sensor_name = new_name
        logging.info(f"Sensor name changed to '{new_name}'")

    '''def start(self):
        try:
            logging.info("Sensor data generation started")
            while True:
                data = self.generate_data()
                if data:
                    self.send_data_to_broker(data)
                time.sleep(self.data_generation_interval)
        except KeyboardInterrupt:
            logging.info("Stopping sensor data generation...")
            self.sock_data.close()
            self.sock_cmd.close()'''
    
    def start(self):
        try:
            # Tentar se conectar ao broker e registrar-se
            self.register_with_broker()

            logging.info("Sensor data generation started")
            while True:
                data = self.generate_data()
                if data:
                    self.send_data_to_broker(data)
                time.sleep(self.data_generation_interval)

        except Exception as e:
            logging.error(f"Error in sensor operation: {e}")
            logging.info("Attempting to reconnect and register...")

            # Tentar se reconectar e registrar em um loop separado
            self.reconnect_and_register_loop()

    def reconnect_and_register_loop(self):
        while True:
            try:
                # Tentar se reconectar e registrar com o broker
                self.register_with_broker()

                logging.info("Reconnected and registered with broker")
                break  # Sair do loop se a reconexão for bem-sucedida

            except Exception as e:
                logging.error(f"Error in reconnection process: {e}")
                time.sleep(5)  # Esperar um tempo antes de tentar reconectar

    def register_with_broker(self):
        try:
            self.sock_cmd.connect((self.server_host, self.server_port))
            registration_message = {"type": "register", "name": self.sensor_name}
            self.sock_cmd.send(json.dumps(registration_message).encode())
            logging.info(f"Sensor '{self.sensor_name}' registered with broker")
            threading.Thread(target=self.receive_commands).start()  # Inicia uma thread para receber comandos em segundo plano
        except Exception as e:
            logging.error(f"Error registering with broker: {e}")

    def receive_commands(self):
        try:
            logging.info(f"Sensor '{self.sensor_name}' waiting for commands...")
            while True:
                command = self.sock_cmd.recv(1024).decode()
                if not command:
                    print("Empty command received from broker")
                    break
                logging.info(f"Command received by sensor '{self.sensor_name}': {command}")
                self.process_command(command)
        except Exception as e:
            logging.error(f"Error receiving commands: {e}")

    def process_command(self, command):
        if command == "turn_on":
            self.turn_on()
        elif command == "turn_off":
            self.turn_off()
        elif command == "restart":
            self.restart()
        elif command == "get_temperature":  # Responder ao comando de obtenção de dados
            data = self.generate_data()
            if data:
                print("\n\n\n\n\t ta indo")
                self.send_data_to_broker(data)
                print("\n\n\n\n\t ta indo o envio \n\n")
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

    def stop(self):
        try:
            self.sock_data.close()
            self.sock_cmd.close()
            logging.info("Sensor stopped")
        except Exception as e:
            logging.error(f"Error stopping sensor: {e}")

def menu():
    print("\nMenu:")
    print("1. Ligar")
    print("2. Desligar")
    print("3. Trocar nome do sensor")
    print("5. Sair")

    choice = input("Escolha uma opção: ")
    return choice

if __name__ == "__main__":
    server_ip = input("IP do Servidor para se registrar: ")
    data_server_port = 9999
    broker_port = 9998
    sensor_name = "TemperatureSensor"

    sensor = VirtualSensor(server_ip, data_server_port, server_ip, broker_port, sensor_name)

    # Iniciar o dispositivo e conectar ao broker
    sensor_thread = threading.Thread(target=sensor.start)
    sensor_thread.start()

    # Exibir o menu de controle
    while True:
        choice = menu()

        if choice == "1":
            if not sensor.is_on:
                sensor.turn_on()
            else:
                print("O sensor já está ligado.")
        elif choice == "2":
            if sensor.is_on:
                sensor.turn_off()
            else:
                print("O sensor já está desligado.")
        elif choice == "3":
            new_name = input("Digite o novo nome para o sensor: ")
            sensor.change_sensor_name(new_name)
        elif choice == "5":
            print("Encerrando...")
            sensor.stop()  # Adicione uma função stop() para encerrar o dispositivo
            break
        else:
            print("Opção inválida. Tente novamente.")
