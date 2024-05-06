import React, { useState, useEffect } from "react";
import { IP } from "./IP";

function MainRightTopCard() {
  const [lastCommand, setLastCommand] = useState("");

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

  // Atualizar o último comando periodicamente
  useEffect(() => {
    const interval = setInterval(fetchLastCommand, 1000); // Atualizar a cada 5 segundos
    return () => clearInterval(interval); // Limpar o intervalo quando o componente for desmontado
  }, []); // Sem dependências, portanto, apenas executa uma vez

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
          Avisos 
        </p>
      </div>
    </div>
  );
}

export default MainRightTopCard;
