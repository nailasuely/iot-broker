import React from "react";

function MainRightTopCard() {
  return (
    <div className="topCard">
      <div className="topCard_name">
        <h2>Estatísticas</h2>
      </div>

      <div className="earning">
        <p>
          Dispositivo Conectados <span>187</span>
        </p>

        <p>
          Dispositivos Ligados <span>5</span>
        </p>

        <p>
          Dispositivos Desligados <span>25</span>
        </p>

        <p>
          Quantidade <span>200</span>
        </p>

        <p>
          Total <span>262 ETH</span>
        </p>
      </div>
    </div>
  );
}

export default MainRightTopCard;
