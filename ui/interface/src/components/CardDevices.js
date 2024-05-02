/*import projImg1 from "../assets/img/img-view3.png";
import React from "react";
import TopSeller from "./TopSeller";
import "./MainContainer.css";

function CardDevices({ devices }) {
    return (
      <div className="bottom_card">
        <div className="bottomCard_name">
          <h2>Dispositivos Conectados</h2>
        </div>
  
        {Array.isArray(devices) && devices.length > 0 ? (
          devices.map((device, index) => (
            <div className="topSeller" key={index}>
              <div className="topSellerImg">
                <img src={projImg1} alt="" />
              </div>
              <div className="topSellerName">
                
                  {device}
                
              </div>
              <a href="#" className="button btm">
                Alterar nome
              </a>

            </div>
          ))
        ) : (
          <p>Nenhum dispositivo encontrado</p>
        )}
      </div>
    );
  }
  
  export default CardDevices;
  */


import projImg1 from "../assets/img/img-view3.png";
import React, { useState } from 'react';
import "./MainContainer.css";
import { DeviceName } from './DeviceName'; // Importe o componente DeviceName


function CardDevices({ devices }) {
    const [currentDevice, setCurrentDevice] = useState(null);
    const [showDeviceName, setShowDeviceName] = useState(false); // Novo estado para controlar a exibição do componente DeviceName

    const handleNameChangeClick = (deviceName) => {
        setCurrentDevice(deviceName);
        setShowDeviceName(true); // Mostra o componente DeviceName quando o botão "Alterar nome" é clicado
    };

    const handleBackClick = () => {
        setCurrentDevice(null);
        setShowDeviceName(false); // Volta para a lista de dispositivos quando o botão "Voltar" é clicado
    };

    const handleDeviceNameSubmit = () => {
      setTimeout(() => {
        setShowDeviceName(false); // Volta para a lista de dispositivos após um segundo
      }, 1000);
    };

    return (
        <div className="bottom_card">
            {showDeviceName ? (
                <DeviceName deviceName={currentDevice} onSubmit={handleDeviceNameSubmit} />
            ) : (
                <div >
                    <h4>Dispositivos Conectados</h4>
                    {Array.isArray(devices) && devices.length > 0 ? (
                        devices.map((device, index) => (
                            <div className="topSeller" key={index}>
                                <div className="topSellerImg">
                                    <img src={projImg1} alt="" />
                                </div>
                                <div className="topSellerName">
                                    {device}
                                </div>
                                <a className="button btm">
                                <button onClick={() => handleNameChangeClick(device)}>Alterar nome</button>
                                </a>
                            </div>
                        ))
                    ) : (
                        <p>Nenhum dispositivo encontrado</p>
                    )}
                </div>
            )}
        </div>
    );
}

export default CardDevices;
