
<h1 align="center">
  <br>
    <img width="400px" src="https://github.com/nailasuely/iot-broker/assets/98486996/5eae8d55-cf1b-47ed-985e-41fc27c450d9"> 
  <br>
  Internet das Coisas
  <br>
</h1>


<h4 align="center">Projeto da disciplina TEC 502 - Concorrência e Conectividade </h4>

<p align="center">
<div align="center">

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/nailasuely/iot-broker/blob/main/LICENSE)




> Esse é um projeto da disciplina TEC 502 - Concorrência e Conectividade, no qual ocorre o desenvolvimento de um serviço broker baseado em TCP/IP, facilitando a troca de mensagens entre dispositivos e aplicações. Os componentes foram implementados e testados em contêineres Docker, utilizando sockets TCP/IP e UDP para a comunicação entre dispositivos virtuais e o serviço broker. O sistema permite a interação entre dispositivos e aplicações de forma organizada, facilitando uma comunicação eficiente.


## Download do repositório

```
gh repo clone nailasuely/iot-broker
```

</div>

![-----------------------------------------------------](https://github.com/nailasuely/breakout-problem3/blob/main/assets/img/prancheta.png)

## Sumário

- [Introdução](#Introdução)
- [Tecnologias e Ferramentas Utilizadas](#Tecnologias-e-Ferramentas-Utilizadas)
- [Metodologia](#Metodologia)
  - [Estrutura do Projeto](#Estrutura-do-Projeto)
  - [Broker](#Broker)
  - [Dispositivo virtual](#Dispositivo-Virtual)
  - [Aplicação](#Aplicação)
  - [API RESTful](#Api-restful)
- [Como utilizar](#Como-utilizar)
- [Conclusão](#Conclusão)
- [Equipe](#equipe)
- [Tutor](#tutor)
- [Referências](#referências)

![-----------------------------------------------------](https://github.com/nailasuely/breakout-problem3/blob/main/assets/img/prancheta.png)

## Introdução 

A Internet das Coisas (IoT) ganhou destaque nas últimas décadas ao conectar objetos físicos à internet, permitindo a coleta e compartilhamento de dados de forma remota. Segundo Dias (2016), a IoT refere-se a um conceito revolucionário que transforma objetos comuns em dispositivos inteligentes capazes de coletar, transmitir e receber dados, além de responder a comandos de forma autônoma ou interativa. Essa abordagem, proposta por Dias, reforça a ideia de que a IoT não apenas conecta dispositivos, mas também cria novas oportunidades para automação, monitoramento e controle em uma variedade de setores.

Diante da crescente relevância da IoT, uma empresa direcionou uma startup para desenvolver um serviço que simplifique a comunicação entre dispositivos e aplicações
A proposta  é criar um serviço de broker que facilite a troca de mensagens entre dispositivos e aplicações, utilizando como base o subsistema de rede TCP/IP.

Para atender aos requisitos e restrições do projeto, o desenvolvimento foi realizado utilizando Python para o backend, tanto para o serviço broker quanto para o dispositivo virtual, enquanto a aplicação foi desenvolvida em React para a interface do usuário. A comunicação entre os dispositivos virtuais e o serviço broker foi implementada utilizando a interface de socket nativa do TCP/IP para comandos e UDP para dados, enquanto a comunicação entre o serviço broker e a aplicação foi realizada por meio de uma API RESTful.


## Tecnologias e Ferramentas Utilizadas
- **Python:** Linguagem de programação. 
- **Flask:**  Framework web em Python usado para realizar a implementação a API RESTful.
- **Socket:** Módulo em Python utilizado para a comunicação de rede entre o broker e os dispositivos.
- **Threading:** Módulo em Python utilizado para implementar threads e permitir operações concorrentes.
- **JSON:** Formato de dados utilizado para troca de mensagens entre o broker e os dispositivos.
- **CORS** (Cross-Origin Resource Sharing): Extensão Flask  que é utilizada para permitir solicitações de diferentes origens para API.
- **Postman:** Plataforma para teste e desenvolvimento de APIs,
- **Docker:** Ferramenta para empacotar e distribuir aplicativos em contêineres.

## Metodologia 

A arquitetura da solução foi desenvolvida para proporcionar uma comunicação adequada entre os dispositivos e aplicações. Ela é composta por três principais componentes: o serviço de broker, o dispositivo virtual simulado e a aplicação com interface de usuário (Imagem ??) . Cada um desses componentes desempenha tem o seu papél específico e se comunica de maneira organizada que possibilite a troca de mensagens entre eles. Esses componentes serão detalhados a seguir.

<div align="center">
 <img width="" src="https://github.com/nailasuely/iot-broker/assets/98486996/0c3f65a9-a0ee-4214-b6da-6d9e4f7207e9">
</div>

### Broker 

O serviço de broker funciona como o centro da arquitetura, permitindo a troca de mensagens entre os dispositivos e aplicações. Ele funciona como um intermediário que recebe, roteia e entrega mensagens entre os clientes conectados. Para implementar o Broker, foram desenvolvidas funcionalidades específicas, como inicialização de servidores para receber dados e comandos, registro,  processamento de dados recebidos dos dispositivos, gerenciamento de conexões, entre outros.

Os dispositivos se comunicam com o Broker enviando dados e recebendo comandos. As aplicações também se comunicam com o Broker para enviar comandos aos dispositivos e receber dados dos mesmos. A comunicação entre os dispositivos e o Broker é realizada por meio de conexões UDP para a transmissão de dados e conexões TCP (Transmission Control Protocol) para recepção e envio de comandos.  Por outro lado, a comunicação entre as aplicações e o Broker é realizada por meio de requisições HTTP sobre o protocolo TCP.

A infraestrutura do Broker é feita utilizando múltiplas threads, permitindo o processamento concorrente de múltiplas conexões para possibilitar a recepção de dados e enviar e receber comandos . 

- A ordem das mensagens trocadas no componente Broker é a seguinte:
  1. Recebimento de Dados dos Dispositivos:
      - Os dispositivos enviam dados para o Broker utilizando conexões UDP.
      - O Broker recebe os dados, faz o processamento deles, e os armazena temporariamente em um dicionário de dados.
      - Em paralelo, com uso de thread,  o Broker encaminha os dados recebidos para as aplicações interessadas através de conexões TCP.
  2. Envio de Comandos pelas Aplicações:
      -  As aplicações enviam comandos para o Broker utilizando requisições HTTP sobre o protocolo TCP (Transmission Control Protocol). 
      - O Broker recebe os comandos, faz a interpretação adequada, e executa as operações correspondentes, como registro de dispositivos, envio de comandos para dispositivos e outros métodos necessários.,
  3. Transmissão de Respostas para Dispositivos e Aplicações:
      - Os comandos para os dispositivos são enviados usando conexão TCP. 
      - Já as respostas para as aplicações são transmitidas via HTTP sobre TCP, fornecendo a confiabilidade da comunicação.
        
#### - Funcionamento do broker (broker.py) 

As principais funções do broker são as seguintes:

1. **`setup_data_server`**:
  - Essa função configura um servidor UDP para receber dados dos dispositivos. O método `bind` associa o socket a um endereço IP e porta para receber os dados. Após a configuração, o servidor fica esperando pelos dados dos dispositivos.

2. **`setup_command_server`**:
  - Aqui é configurado um servidor TCP para receber comandos das aplicações. O método `listen` faz com que o socket aceite conexões, definindo um limite máximo de conexões pendentes.

3. **`processData`**:
   - Esta função é executada em uma thread separada para processar os dados recebidos dos dispositivos. Utiliza um loop infinito para aguardar a chegada de dados no socket UDP. Quando os dados chegam, são decodificados usando JSON (JavaScript Object Notation). Em seguida, os dados são armazenados em um dicionário paa enviar depois para aplicações.

4. **`manageDeviceConnection`**:
   - Essa função é usada para gerenciar a conexão com os dispositivos. Ela recebe conexões de dispositivos e processa os comandos enviados por eles. Utiliza uma estrutura de loop para receber dados do dispositivo e processá-los conforme o tipo de comando. Caso a conexão seja encerrada abruptamente (fechando a janela ou algo do tipo), o dispositivo é removido do registro.

5. **`send_command_to_device`**:
   - Esta função envia comandos para dispositivos específicos. Ela utiliza a conexão TCP estabelecida com o dispositivo para enviar o comando desejado. O comando é codificado em bytes e enviado através da conexão TCP. Isso permite que as aplicações enviem comandos para controlar os dispositivos conectados ao broker.

Além disso, a função `start_escutarDados` é responsável por escutar continuamente os dados dos dispositivos, paea que o broker sempre esteja pronto para receber informações.E a função `manageDeviceConnectio` precisa lidar com múltiplas conexões de dispositivos de forma simultânea, permitindo que o broker gerencie diversas interações ao mesmo tempo. Assim, essas operações ocorrem em threads separadas para evitar bloqueios, garantindo assim a capacidade de resposta do sistema mesmo diante de múltiplas requisições concorrentes. 


### Dispositivo virtual (sensor e atuador)

O componente "dispositivo", representado pela classe `VirtualSensor` tem o intuito de representar o sensor e atuador. Para realizar esse papel, ele encapsula a lógica de um sensor virtual, que simula a função de um sensor real, gerando dados de temperatura e enviando esses dados para o broker. 

Para poder realizar esse papel, o dispositivo utiliza dois protocolos de comunicação diferentes. Para o envio dos dados gerados, ele utiliza o protocolo UDP (User Datagram Protocol) que foi proposto como uma forma não confiável de enviar dados,  e para receber comandos do broker e manter uma comunicação bidirecional, ele utiliza o protocolo TCP (Transmission Control Protocol), que oferece confiabilidade na entrega dos dados. Ele pode gerar esses dados de forma assíncrona em uma thread separada, garantindo que a coleta de dados não ocasione em problemas com outras operações. Ele também possui uma função de registro com o broker, no qual se conecta inicialmente para anunciar sua presença na rede e estabelecer a comunicação.

#### - Funcionamento do dispositivo (dispositivo.py) 
1. **`__init__`:** Este método inicializa a classe do dispositivo com os primeiros parâmetros necessários, como o endereço IP e porta do servidor de registro, o endereço IP e porta do broker, e também o nome do sensor. Além disso, ele configura os sockets UDP e TCP para comunicação com o broker e faz o inicio do processo de registro com o broker.

2. **`send_data_to_broker`:** Essa função é responsável por enviar os dados do sensor para o broker usando conexões UDP. Os dados gerados incluem informações como o nome do sensor, os dados de temperatura, o tipo de sensor e o estado que pode ser tanto ligado quanto desligado.

3. **`generate_data`:** Aqui, os dados de temperatura são gerados para o sensor de forma aleatória para simular um sensor de verdade. Se o sensor estiver ligado, ele cria um valor aleatório dentro de dois valores, um mínimo e um máximo, e faz o retorno desse valor como uma string que vai ser enviada em algum momento para o broker. 

4. **`change_sensor_name`:** Esta é a função que permite alterar o nome do sensor. Ela atualiza o nome do sensor localmente e envia uma mensagem de notificação ao broker sobre a mudança de nome para que possa ser atualizado no broker também. 

5. **`change_temperature_range`:** Essa é uma função que faz a alteração do intervalo de temperatura entre o valor mínimo e máximo. Se os novos valores forem válidos, ela os atualiza localmente e envia uma mensagem de notificação ao broker sobre a alteração no intervalo de temperatura.

6. **`start`:** Essa função inicia o sensor e a geração contínua de dados. Ela executa um loop infinito que gera dados periodicamente enquanto o sensor estiver ligado, enviando esses dados para o broker.

7. **`register_with_broker`:** Aqui, o sensor se registra com o broker, tentando estabelecer uma conexão TCP e enviar uma mensagem de registro. Ele continua tentando até que a conexão seja feita de forma correta. 

8. **`receive_commands`:** Essa função recebe comandos do broker por meio de uma conexão TCP separada. Ela opera em uma thread separada para permitir que o dispositivo continue recebendo comandos enquanto gera dados.

9. **`process_command`:** Esta função processa os comandos recebidos do broker, como ligar, desligar, reiniciar o sensor ou alterar o nome do sensor. Dependendo do comando recebido, ele executa que foi requisitada.

10. *Outras funções:* Além de todas essas citadas, também existem as funções para executarem o comando adequado para o dispotivo como `turn_on`, `turn_off` e `restart` que fazem as ações necessárias e enviam uma notificação para o broker avisando que o comando foi feito. 

#### - Gerenciamento do dispositivo

O dispositivo responde comandos enviados de forma remota, usando o broker como intermediário, e também de maneira local, no qual o usuário escolhe o que deseja fazer no dispositivo diretamente. Quando um comando é enviado ao dispositivo, para ligar, desligar, reiniciar, alterar o nome ou alterar o intervalo de dados (Imagem), ele processa esse comando e executa o comando por uma das funções disponíveis. Por exemplo, se por acaso ele receber um comando de ligar, ele ativa a geração de dados e começa a enviar as informações de temperatura ao broker. Da mesma forma, se o comando for para alterar o nome do dispositivo, ele atualiza o nome localmente e notifica o broker sobre essa mudança. 

<div align="center">
 <img width="" src="https://github.com/nailasuely/iot-broker/assets/98486996/6da68269-444b-4056-ad46-1fa27bc63408">
</div>

Os comandos disponíveis para o dispositivo são esses: 

1. Ligar: Liga o sensor e envia informações de temperatura ao broker.
2. Desligar: Interrompe a geração de dados do sensor e para de enviar informações ao broker.
3. Reiniciar: Desliga e liga novamente o sensor, reiniciando o processo de geração de dados.
4. Alterar o nome: Permite mudar o nome do sensor, fazendo a atualização localmente e notificando o broker sobre a alteração.
5. Alterar o intervalo: Trocar o intervalo de geração de dados. 
6. Sair: Parar a execução do dispositivo e se desconecta totalmente com o broker.
   

  
### Comunicação entre dispositivo e Broker

Como falado anteriormente, entre e o Broker, dois protocolos de comunicação foram escolhidos: UDP e TCP. O protocolo UDP é utilizado para a transmissão de dados do sensor para o Broker. Essa comunicação é realizada de forma não confiável e sem conexão direta entre as partes, o que é uma escolha adequada para o envio de dados em tempo real. Já o protocolo TCP é usado para o envio de comandos do Broker para os dispositivos visto que oferece uma comunicação mais confiável orientada a conexão.

<div align="center">
  
| Tipo de Comunicação | Protocolo | Descrição                                              |
|----------------------|-----------|--------------------------------------------------------|
| Envio de Dados       | UDP       | Utilizado para enviar dados dos dispositivos para o Broker. |
| Comandos             | TCP       | Utilizado para enviar comandos do Broker para os dispositivos. |

</div>

### API RESTful

A interface da aplicação faz a utilização do padrão REST (Representational State Transfer) para definir as rotas e o HTTP utilizados na comunicação entre o cliente (no sistema,  um cliente seria outra aplicação ou um usuário acessando pelo navegador) e o servidor (implementado pelo broker, utilizando a biblioteca Flask presente do Python). Assim, abaixo está uma tabela com as rotas que podem ser utilizadas, seguidas respectivamente pelo método, o protocolo e uma pequena descrição do que cada rota faz. 

<div align="center">
  
| Rota                                    | Método | Protocolo | Descrição                                                                                                          |
|-----------------------------------------|--------|-----------|--------------------------------------------------------------------------------------------------------------------|
| /devices                                | GET    | HTTP      | Retorna uma lista de dispositivos registrados no sistema, representados pelos seus nomes, em formato JSON.        |
| /devices/<device_name>/name             | PUT    | HTTP      | Permite alterar o nome de um dispositivo registrado no sistema. |
| /devices/<device_name>/data             | GET    | HTTP      | Obtém os dados de um dispositivo registrado. Ele precisa receber o nome do dispositivo na rota e retorna os dados associados a esse dispositivo em formato JSON caso ele esteja registrado. |
| /devices/<device_name>/command          | POST   | HTTP      | Envia um comando para um dispositivo registrado no sistema. Recebe o nome do dispositivo na rota e o comando no corpo da requisição. |
| /last_command                           | GET    | HTTP      | Retorna a última operação realizada no sistema|

</div>

  
Após enviar a requisição corretamente, o cliente recebe códigos de status HTTP que são retornados como parte das respostas do protocolo. Eles são importantes para comunicar o estado da operação ao cliente que fez a solicitação. A tabela a seguir mostra esses códigos: 

<div align="center">
  
| Código | Descrição                                                                                                      |
|--------|----------------------------------------------------------------------------------------------------------------|
| 200    | OK - Requisição foi feita corretamente.                                                                 |
| 400    | Bad Request - Rrro na requisição, como falta de parâmetros ou formato inválido.             |
| 404    | Not Found - Recurso solicitado não foi encontrado no servidor.                                        |

</div>

## Como utilizar

1. Clone ou faça o download do repositório.
2. Use o comando "cd" para seguir o caminho até encontrar a pasta adequada.

###  • Execução do Broker:

1. **Usando Docker:**
    - Vá até o diretório no qual o serviço broker está localizado.
    - Execute o seguinte comando para iniciar o serviço broker:
      
        ```
        docker container run -it --network host broker-service
        ```
  
2. **Execução Convencional:**
    - Vá até o diretório no qual o serviço broker está localizado.
    - Execute o seguinte comando para iniciar o serviço broker:
      
        ```
       python3 broker.py
        ```

### • Execução dos Dispositivos Virtuais:
  2. **Execução Convencional:**
     - Após iniciar o serviço broker, abra um novo terminal em sua própria máquina ou em outra que contém o dispositivo. 
     - Execute o seguinte comando:
       
          ```
         python3 Nome_do_Dispositivo.py 
          ```
        
     - Logo em seguida o dispositivo irá perguntar o IP do broker e o nome do dispositivo.
     - Insira o IP do broker.
     - Insira o nome do dispositivo. 

### • Execução dos Aplicação (com interface):
1. **Usando Docker:**
    - Vá até o diretório no qual a interface está localizada.
    - Execute o seguinte comando para iniciar o serviço broker:
      
        ```
        docker compose up client --build
        ```
        
2. **Execução Convencional:**
    - Vá até o diretório no qual a interface está localizada.
    - Você precisa ter todas as dependências instaladas.
      
        ```
        npm install
        ```
        
   - Inicie a execução com seguinte linha de comando:
     
        ```
        npm start
        ```
        
### Execução pelo Postman:
1. **Abra o Postman:**

2. **Importe a Coleção:**
   - Importe a [coleção](https://github.com/nailasuely/iot-broker/blob/main/Arquivo%20de%20Testes.postman_collection.json) de requests no formato JSON.
     
3. **Execute as Requests:**
   - Dentro da coleção importada, existem algumas requests para testar a API.
   - Selecione a request que deseja executar.
   - Clique no botão "Send" para enviar a request.
   - Visualize as respostas. 

![-----------------------------------------------------](https://github.com/nailasuely/breakout-problem3/blob/main/assets/img/prancheta.png)

## Equipe

[//]: contributor-faces

<a href="https://github.com/nailasuely"><img src="https://github.com/nailasuely/breakout-problem3/blob/main/assets/img/naila.png" title="naila" width="100"></a>

[//]: contributor-faces


## Tutor

<div style="display:flex;">
    <a href="https://github.com/x-anf" style="display: inline-block; border: none;">

   
</div>


## Referências 
> - [1] 
> - [2] 
