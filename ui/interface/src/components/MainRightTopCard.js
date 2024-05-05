import React from "react";

function MainRightTopCard({ rawData }) {
  console.log(rawData)
  return (
    <div className="topCard">
      <div className="topCard_name">
        <h2>Estatísticas</h2>
      </div>

      <div className="earning">
        <p>
          Dispositivo Ligados <span>187</span>
        </p>

        <p>
          Dispositivos Desligados <span>5</span>
        </p>

        <p>
          Dispositivos Conectados <span>25</span>
        </p>
      </div>
    </div>
  );
}

export default MainRightTopCard;
