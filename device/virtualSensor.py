import logging
import threading
import socket
import json
import time
import random
import ipaddress


# comandos p eu nao esquecer
#docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' fab528579903
# cat broker.log

# como usar o loggind: https://docs.python.org/3/library/logging.html

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s - %(message)s')

class VirtualSensor:
    def __init__(self, ipServer, serverPort, ipBroker, brokerPort, sensor_name):
        self.ipServer = ipServer
        self.serverPort = serverPort
        self.ipBroker = ipBroker
        self.brokerPort = brokerPort
        self.sensor_name = sensor_name
        self.timeDatas = 1

        # udp para dados
        self.data_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # tcp para comandos
        self.commands_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.min_value = 0
        self.max_value = 50

        self.sensor_type = "Temperature"
        self.is_on = True
        self.registerWithBroker()

    def sendDataBroker(self, data):
        message = {"source": self.sensor_name, "data": data}
        try:
            self.data_socket.sendto(json.dumps(message).encode(), (self.ipBroker, self.brokerPort))
            logging.info(f"Sensor '{self.sensor_name}' sent data to broker: {data}")
        except Exception as e:
            logging.error(f"Error sending data to broker: {e}")

    def generate_data(self):
        if self.is_on:
            if self.sensor_type == "Temperature":
                data_value = round(random.uniform(self.min_value, self.max_value), 2)
                return f"{data_value}"
        return ""

    def start(self):
        try:
            logging.info("Sensor data generation started")
            while True:
                data = self.generate_data()
                if data:
                    self.sendDataBroker(data)
                time.sleep(self.timeDatas)
        except KeyboardInterrupt:
            logging.info("Stopping sensor data generation...")
            self.data_socket.close()
            self.commands_socket.close()

    def registerWithBroker(self):
        try:
            self.commands_socket.connect((self.ipServer, self.serverPort))
            registration_message = {"type": "register", "name": self.sensor_name}
            self.commands_socket.send(json.dumps(registration_message).encode())
            logging.info(f"Sensor '{self.sensor_name}' registered with broker")
            threading.Thread(target=self.receive_commands).start()  # Inicia uma thread para receber comandos em segundo plano
        except Exception as e:
            logging.error(f"Error registering with broker: {e}")

    def receive_commands(self):
        try:
            logging.info(f"Sensor '{self.sensor_name}' waiting for commands...")
            while True:
                command = self.commands_socket.recv(1024).decode()
                if not command:
                    print("Empty command received from broker")
                    break
                logging.info(f"Command received by sensor '{self.sensor_name}': {command}")
                self.processCommand(command)
        except Exception as e:
            logging.error(f"Error receiving commands: {e}")

    def processCommand(self, command):
        if command == "turnON":
            self.turnON()
        elif command == "turnOFF":
            self.turnOFF()
        elif command == "restart":
            self.restart()

        # isso eu tirei por conta que tava dando mt problema no broker e coloquei direto no http
        elif command == "get_temperature":  # Responder ao comando de obtenção de dados
            data = self.generate_data()
            if data:
                print("\n\n\n\n\t ta indo")
                self.sendDataBroker(data)
                print("\n\n\n\n\t ta indo o envio \n\n")
        else:
            logging.error("Invalid command")

    def turnON(self):
        self.is_on = True
        logging.info("Sensor turned on")

    def turnOFF(self):
        self.is_on = False
        logging.info("Sensor turned off")

    def restart(self):
        self.turnOFF()
        time.sleep(1)
        self.turnON()
        logging.info("Sensor restarted")

def validIP(ip_validar):
    while True:
        try:
            ip = input(ip_validar)
            ipaddress.ip_address(ip)
            return ip
        except ValueError:
            print("Por favor, insira um endereço IP válido.")


if __name__ == "__main__":
    server_ip = validIP("IP do Servidor para se registrar: ")
    data_serverPort = 9999
    brokerPort = 9998
    ipBroker = validIP("IP do broker para enviar dados: ")
    sensor_name = "TemperatureNaila"

    sensor = VirtualSensor(server_ip, data_serverPort, ipBroker, brokerPort, sensor_name)
    sensor.start()