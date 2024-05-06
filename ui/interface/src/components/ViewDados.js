import React from "react";

function MainRightBottomCard({ rawData }) {  
  //console.log(rawData)
  
  return (
    <div className="bottom_card">
      <div className="bottomCard_name">
        <h2>Todos os dispositivos</h2>
      </div>
      {Array.isArray(rawData) && rawData.length > 0 ? (
        rawData.map((data, index) => (
          <div className="topSeller" key={index}>
            <div className="topSellerName">
              <h3>Dispositivo: {data?.source}</h3>
            </div>
            <div className="topSellerName">
              <p>Data: {data?.data}</p>
              <p>Hora: {data?.time}</p>
              <p>Tipo: {data?.type}</p>
              <p>Estado: {data?.state}</p>
            </div>
          </div>
        ))
      ) : (
        <p>Nenhum dispositivo encontrado</p>
      )}
    </div>
  );
}

export default MainRightBottomCard;
