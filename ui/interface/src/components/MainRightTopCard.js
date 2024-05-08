import React, { useState, useEffect } from "react";
import { IP } from "./IP";

function MainRightTopCard() {
  const [lastCommand, setLastCommand] = useState("");
  const [aviso, setAviso] = useState("");

  // Função para obter o último comando
  const fetchLastCommand = async () => {
    try {
      const response = await fetch(`http://${IP}:5001/last_command`);
      const data = await response.json();
      const { last_command } = data;

      if (last_command) {
        // Formatar o comando de acordo com o tipo
        switch (last_command.type) {
          case "register":
            setLastCommand(`O sensor ${last_command.device_name} se registrou.`);
            break;
          case "change_name":
            setLastCommand(`O dispositivo ${last_command.device_name} alterou seu nome.`);
            break;
          case "shutdown":
            setLastCommand(`O dispositivo ${last_command.device_name} foi desligado.`);
            break;
            case "restart":
              setLastCommand(`O dispositivo ${last_command.device_name} foi reiniciado.`);
              break;
            case "turn_on":
              setLastCommand(`O dispositivo ${last_command.device_name} foi ligado.`);
              break;
            case "turn_off":
              setLastCommand(`O dispositivo ${last_command.device_name} foi desligado.`);
              break;
          default:
            setLastCommand("Comando desconhecido recebido.");
        }
      }
    } catch (error) {
      console.error("Erro ao obter o último comando:", error);
    }
  };

  const fetchAviso = async () => {
    try {
      const response2 = await fetch(`http://${IP}:5001/avisos`);
      const data2 = await response2.json();
      const { aviso } = data2;
      if (aviso) {
        // Formatar o comando de acordo com o tipo
        switch (aviso.type) {
          case "inatividade":
            setAviso(`O sensor ${aviso.device_name} está inativo.`);
            break;
          default:
            setAviso("Sem avisos");
        }
      }
    } catch (error) {
      console.error("Erro ao obter o aviso:", error);
    }
  };

  /*
  // Atualizar o último comando
  useEffect(() => {
    const interval = setInterval(fetchLastCommand, 1000); // 1 segundinho
    return () => clearInterval(interval); 
  }, []); //  apenas executa uma vez
*/

  useEffect(() => {
    const intervalLastCommand = setInterval(fetchLastCommand, 1000);
    const intervalAviso = setInterval(fetchAviso, 1000);
    
    return () => {
      clearInterval(intervalLastCommand);
      clearInterval(intervalAviso);
    };
  }, []);


  return (
    <div className="topCard">
      <div className="topCard_name">
        <h2>Estatísticas</h2>
      </div>

      <div className="earning">
        <p>
          Último comando recebido: 
        </p>
        <p className="lastCommandText">
          {lastCommand}
        </p>
        <p>
          Avisos: 
        </p>
        <p className="lastCommandText">
          {aviso}
        </p>
      </div>
    </div>
  );
}

export default MainRightTopCard;
