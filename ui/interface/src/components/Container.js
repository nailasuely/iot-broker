import React from "react";
import "./Container.css";
import MainContainer from "./MainContainer";

function Contain({datas, devices, projects, devicesDatas}) {
  return (
    <div className="container">
      <MainContainer datas={datas} devices= {devices} projects={projects} devicesDatas={devicesDatas}/>
    </div>
  );
}

export default Contain;
