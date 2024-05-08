
<h1 align="center">
  <br>
    <img width="400px" src="https://github.com/nailasuely/iot-broker/blob/main/assets/gif_logo.gif"> 
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
  - [Comunicação entre dispositivo, broker e aplicação](#Comunicação-entre-dispositivo,-broker-e-aplicação)
  - [API RESTful](#Api-restful)
- [Testes](#Testes)
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

![-----------------------------------------------------](https://github.com/nailasuely/breakout-problem3/blob/main/assets/img/prancheta.png)

## Tecnologias e Ferramentas Utilizadas
- **Python:** Linguagem de programação. 
- **Flask:**  Framework web em Python usado para realizar a implementação a API RESTful.
- **Socket:** Módulo em Python utilizado para a comunicação de rede entre o broker e os dispositivos.
- **Threading:** Módulo em Python utilizado para implementar threads e permitir operações concorrentes.
- **JSON:** Formato de dados utilizado para troca de mensagens entre o broker e os dispositivos.
- **CORS** (Cross-Origin Resource Sharing): Extensão Flask  que é utilizada para permitir solicitações de diferentes origens para API.
- **Postman:** Plataforma para teste e desenvolvimento de APIs,
- **Docker:** Ferramenta para empacotar e distribuir aplicativos em contêineres.

![-----------------------------------------------------](https://github.com/nailasuely/breakout-problem3/blob/main/assets/img/prancheta.png)

## Metodologia 

<div align="center">
 <img width="800px" src="https://github.com/nailasuely/iot-broker/blob/main/assets/componentes.svg">
  <p> Fig 1. Componentes do Sistema </p>
</div>

A arquitetura da solução foi desenvolvida para proporcionar uma comunicação adequada entre os dispositivos e aplicações. Ela é composta por três principais componentes: o serviço de broker, o dispositivo virtual simulado e a aplicação com interface de usuário (Figura 2) . Cada um desses componentes desempenha tem o seu papél específico e se comunica de maneira organizada que possibilite a troca de mensagens entre eles. Esses componentes serão detalhados a seguir.

<div align="center">
 <img width="" src="https://github.com/nailasuely/iot-broker/assets/98486996/0c3f65a9-a0ee-4214-b6da-6d9e4f7207e9">
  <p> Fig 2. Estrutura das pastas para organização dos componentes </p>
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
  <p> Fig 3. Menu local do dispositivo </p>
</div>

Os comandos disponíveis para o dispositivo são esses: 

1. Ligar: Liga o sensor e envia informações de temperatura ao broker.
2. Desligar: Interrompe a geração de dados do sensor e para de enviar informações ao broker.
3. Reiniciar: Desliga e liga novamente o sensor, reiniciando o processo de geração de dados.
4. Alterar o nome: Permite mudar o nome do sensor, fazendo a atualização localmente e notificando o broker sobre a alteração.
5. Alterar o intervalo: Trocar o intervalo de geração de dados. 
6. Sair: Parar a execução do dispositivo e se desconecta totalmente com o broker.

### Aplicação 

A aplicação funciona como um painel de controle para dispositivos IoT, no qual os usuários podem visualizar informações e interagir com os dispositivos. Com um sistema de abas, os usuários podem alternar entre diferentes visualizações, como um dashboard e uma lista de dispositivos.

</p>
<div align="center">
   <img width="800px" src="https://github.com/nailasuely/iot-broker/blob/main/assets/Captura%20de%20tela%202024-05-07%20212525.png" />
    <p> Fig 4. Aplicação esperando a conexão do broker</p>
</div>

</p>
<div align="center">
   <img width="800px" src="https://github.com/nailasuely/iot-broker/blob/main/assets/Captura%20de%20tela%202024-05-07%20212801.png" />
    <p> Fig 5. Broker conectado sem dispositivos registrados </p>
</div>

</p>
<div align="center">
   <img width="800px" src="https://github.com/nailasuely/iot-broker/blob/main/assets/Captura%20de%20Tela%20(8).png" />
    <p> Fig 6. Três Dispositivos Conectados </p>
</div>

A interface é construída usando componentes do React Bootstrap. Os dispositivos são representados por cartões, que exibem seu título e uma imagem associada. Além disso, são exibidos os dados correspondentes a cada dispositivo, permitindo aos usuários monitorar o status (conectado ou não conectado) 

Para manter as informações dos dispositivos atualizadas, a aplicação realiza chamadas periódicas para o servidor utilizando o método `fetchData`. Essas chamadas são feitas a cada segundo, garantindo que os dados exibidos na interface estejam sempre atualizados.

O tratamento de erros é feito também para lidar com situações em que as requisições para o servidor falham. Mensagens de erro são exibidas no console do navegador, fornecendo informações úteis para a depuração e identificação de problemas de comunicação.

### Comunicação entre dispositivo, broker e aplicação

<div align="center">
 <img width="800px" src="https://github.com/nailasuely/iot-broker/blob/main/assets/diagrama.svg">
  <p> Fig 7. Comunicação entre os componentes </p>
</div>

No diagrama (Figura 7), é visto algumas das principais funções que possibitam o processo de envio de dados do dispositivo para o broker e o encaminhamento desses dados para a aplicação. Ao iniciar o broker, ocorrem as configurações do servidor de dados e do servidor de comandos, iniciando também as principais threads responsáveis por escutar os dados e gerenciar as conexões, incluindo escutar as respostas e registros de dispositivos.

Olhando agora pelo lado do dispositivo, sua primeira tarefa é solicitar o endereço IP do servidor (broker) ao qual deseja se conectar. Em seguida, tenta se registrar no broker, e enquanto essa operação não é feita, continua tentando se conectar a cada cinco segundos. Após o registro, o dispositivo estabelece a comunicação e inicia uma thread para receber comandos e outra para enviar dados continuamente.

Por fim, a aplicação desempenha o papel de enviar solicitações constantes para acessar os dados disponíveis no broker, completando assim o ciclo de comunicação entre os dispositivos, o broker e a aplicação.

- Camada de Transporte
  Como falado anteriormente, entre e o Broker, dois protocolos de comunicação foram escolhidos: UDP e TCP. O protocolo UDP é utilizado para a transmissão de dados do sensor para o Broker. Essa comunicação é realizada de forma não confiável e sem conexão direta entre as partes, o que é uma escolha adequada para o envio de dados em tempo real. Já o protocolo TCP é usado para o envio de comandos do Broker para os dispositivos visto que oferece uma comunicação mais confiável orientada a conexão.

<div align="center">


| Tipo de Comunicação | Protocolo | Descrição                                              |
|----------------------|-----------|--------------------------------------------------------|
| Envio de Dados       | UDP       | Utilizado para enviar dados dos dispositivos para o Broker. |
| Comandos             | TCP       | Utilizado para enviar comandos do Broker para os dispositivos. |
</div>

- Camada de Aplicação
  Na camada de aplicação, os dispositivos e o Broker se comunicam trocando mensagens no formato JSON. Essas mensagens possuem informações sobre os dados do sensor, comandos a serem executados e notificações sobre o estado do dispositivo. O dispositivo organiza essas mensagens em pacotes de dados e transmite pela rede para o Broker.
  
  No diálogo entre o dispositivo e o broker, o processo começa com uma mensagem de registro enviada pelo dispositivo para o broker. Esta mensagem contém informações como o tipo do dispositivo, seu nome e seu estado (ligado ou desligado). Em seguida, o dispositivo envia regularmente mensagens de dados para o broker. Cada mensagem inclui o nome do dispositivo como fonte, os dados coletados, o tempo da coleta, o tipo de sensor e o estado atual do dispositivo. Essas mensagens são essenciais para manter o broker atualizado com as informações mais recentes dos dispositivos, permitindo que a aplicação acesse dados em tempo real.

<div align="center">
   <img width="600px" src="https://github.com/nailasuely/iot-broker/blob/main/assets/Captura%20de%20tela%202024-05-07%20201408.png" />
    <p> Fig 8. Mensagem de registro </p>
</div>

</p>

<div align="center">
   <img width="600px" src="https://github.com/nailasuely/iot-broker/blob/main/assets/Captura%20de%20tela%202024-05-07%20200447.png" />
    <p> Fig 9. Mensagem de Dados </p>
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


-  Rota: `/devices`
    -   Método: GET

      ``` bash
      curl -X GET http://ip-do-servidor:5001/devices
      ```
    
- Rota: `/devices/<device_name>/name`
  - Método: PUT
    #### Corpo da requisição:
    ```json
    {
        "new_name": "Novo Nome do Dispositivo"
    }
    ```
    ---
    
    ```bash
    curl -X PUT -H "Content-Type: application/json" -d '{"new_name": "Novo Nome do Dispositivo"}' http://ip-do-servidor:5001/devices/NomeAntigoDoDispositivo/name
    ```
- Rota: `/devices/<device_name>/data`
  -  Método: GET
  #### Como usar:
  
  ```bash
  curl -X GET http://ip-do-servidor:5001/devices/NomeDoDispositivo/data
  ```
  ---
  
- Rota: `/devices/<device_name>/command`
  - Método: POST
  
  #### Corpo da requisição:
  ```json
  {
      "command": "turn_on"
  }
  ```
  ---
  
  ```bash
  curl -X POST -H "Content-Type: application/json" -d '{"command": "turn_on"}' http://ip-do-servidor:5001/devices/NomeDoDispositivo/command
  ```

  ---

- Rota: `/last_command`
  - Método: GET
    ```bash
    curl -X GET http://ip-do-servidor:5001/last_command
    ```

Após enviar a requisição corretamente, o cliente recebe códigos de status HTTP que são retornados como parte das respostas do protocolo. Eles são importantes para comunicar o estado da operação ao cliente que fez a solicitação. A tabela a seguir mostra esses códigos: 

<div align="center">
  
| Código | Descrição                                                                                                      |
|--------|----------------------------------------------------------------------------------------------------------------|
| 200    | OK - Requisição foi feita corretamente.                                                                 |
| 400    | Bad Request - Rrro na requisição, como falta de parâmetros ou formato inválido.             |
| 404    | Not Found - Recurso solicitado não foi encontrado no servidor.                                        |

</div>

![-----------------------------------------------------](https://github.com/nailasuely/breakout-problem3/blob/main/assets/img/prancheta.png)

## Testes

Nos testes, além dos realizados diretamente na aplicação React, também foram executados testes utilizando o Postman. Abaixo estão os resultados desses testes realizados por meio do Postman.

<div align="center">
   <img width="600px" src="https://github.com/nailasuely/iot-broker/blob/main/assets/devices.png" />
    <p> Fig 10. Obter dispositivos </p>
</div>

</p>

<div align="center">
   <img width="600px" src="https://github.com/nailasuely/iot-broker/blob/main/assets/novo_nome.png" />
    <p> Fig 11. Alterar nome </p>
</div>

</p>

<div align="center">
   <img width="600px" src="https://github.com/nailasuely/iot-broker/blob/main/assets/obter_dados.png" />
    <p> Fig 12. Obter dados </p>
</div>

</p>

<div align="center">
   <img width="600px" src="https://github.com/nailasuely/iot-broker/blob/main/assets/command_ligar.png" />
    <p> Fig 13. Comando "turn_on" </p>
</div>

</p>

<div align="center">
   <img width="600px" src="https://github.com/nailasuely/iot-broker/blob/main/assets/command_off.png" />
    <p> Fig 14. Comando "turn_off" </p>
</div>

</p>

<div align="center">
   <img width="600px" src="https://github.com/nailasuely/iot-broker/blob/main/assets/command_restart.png" />
    <p> Fig 15. Comando "restart" </p>
</div>

![-----------------------------------------------------](https://github.com/nailasuely/breakout-problem3/blob/main/assets/img/prancheta.png)

## Como utilizar

1. Clone ou faça o download do repositório.
2. Use o comando "cd" para seguir o caminho até encontrar a pasta adequada.

###  • Execução do Broker:

1. **Usando Docker:**
    - Vá até o diretório no qual o serviço broker está localizado.
    - Execute o seguintes comando para iniciar o serviço broker:
      
        ```
        docker build -t broker-service /iot-broker-main/broker
        ```
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
  1. **Usando Docker:**
      - Vá até o diretório devices (iot-broker\device).
      - Execute o seguintes comandos:
      
        ```
         docker build -t device .
        ```
        ```
         docker container run -it --network host device
        ```
  3. **Execução Convencional:**
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
## Conclusão

Por fim, o projeto conseguiu desenvolver um sistema para gerenciar dispositivos IoT, permitindo a comunicação entre os dispositivos, o Broker e a aplicação. Foram implementadas funcionalidades como registro de dispositivos, envio de comandos, obtenção de dados e gerenciamento de conexões.

Durante o desenvolvimento foi adquirida uma compreensão dos princípios de  comunicação de rede, desenvolvimento de APIs RESTful e gerenciamento de conexões em Python. Foi aprendido como aplicar o que foi aprendido em Sistemas Operacionais sobre os conceitos de threads, tratamento de erros e protocolos de comunicação. No entanto, algumas melhorias ainda podem ser feitas, como implementação de autenticação na API para garantir a segurança e melhorar o tratamento de erros e exceções.

Dessa forma, o conhecimento adquirido neste projeto pode ser aplicado tanto em sistemas IoT , quanto em outros cenários de sistema distribuído que exijam comunicação entre dispositivos e servidores. 

![-----------------------------------------------------](https://github.com/nailasuely/breakout-problem3/blob/main/assets/img/prancheta.png)

## Equipe

- Naila Suele

## Tutor

- Antônio A. T. R. Coutinho
   
</div>

![-----------------------------------------------------](https://github.com/nailasuely/breakout-problem3/blob/main/assets/img/prancheta.png)

## Referências 
> - [1] Python Software Foundation. "threading — Thread-based parallelism." Python 3.12.3 documentation. https://docs.python.org/3/library/threading.html. Acessado em 2024.
> - [2] Python Software Foundation. "socket — Low-level networking interface." Python 3.12.3 documentation. https://docs.python.org/3/library/socket.html. Acessado em 2024.
> - [3] Pallets Projects. "Flask Documentation (3.0.x)." Flask. https://flask.palletsprojects.com/en/3.0.x/api/. Acessado em 2024.
> - [4] WebDecoded. "React Project Tutorial: Build a Responsive Portfolio Website w/ Advanced Animations." Acessado em 2024
> - [4] Python Software Foundation. "json — Codificador e decodificador JSON." Python 3.10.2 documentation. https://docs.python.org/3/library/json.html. Acessado em 2024
> - [5] Dias, Gabriel Martins, Boris Bellalta, and Simon Oechsner. "Using data prediction techniques to reduce data transmissions in the IoT." 2016 IEEE 3rd World Forum on Internet of Things (WF-IoT). IEEE, 2016. Acessado em 2024
> - [6] Fabricio Veronez. "Docker do zero ao compose: Parte 01." Transmitido ao vivo em 24 de março de 2022.Youtube, https://www.youtube.com/watch?v=GkMJJkWRgBQ&t=2s. Acessado em 2024 
