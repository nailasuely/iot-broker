
<h1 align="center">
  <br>

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
- [Como utilizar](#Como-utilizar)
- [Tutor](#tutor)
- [Equipe](#equipe)
- [Referências](#referências)

![-----------------------------------------------------](https://github.com/nailasuely/breakout-problem3/blob/main/assets/img/prancheta.png)

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

### • Execução dos Aplicação (com interfaace):
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
