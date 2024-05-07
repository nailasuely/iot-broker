import React from "react";
import "./MainContainer.css";
import Banner from "../assets/img/color-sharp.png";
import MainRightTopCard from "./MainRightTopCard";
import CardDevices from "./CardDevices";
import { Container, Row, Col, Tab, Nav } from "react-bootstrap";
import { ProjectCard } from "./CardView";
import Clock from 'react-live-clock'; 

function MainContainer({ datas, devices, projects, devicesDatas}) {
  //console.log(projects);
  console.log(devicesDatas)
  return (
    <div className="maincontainer">
      <div className="left">
        <div
          className="banner"
          style={{
            background: `url(${Banner})`,
            backgroundRepeat: "no-repeat",
            backgroundSize: "cover",
            backgroundPosition: "center",
          }}
        >
          <div className="textContainer">
            <h1>Dashboard</h1>
            <div className="bid">
              <p>
                Today <Clock format={'dddd, MMMM Do YYYY, h:mm:ss A'} ticking={true} timezone={'America/Sao_Paulo'} />
              </p>
            </div>
          </div>
        </div>

        <div className="cards">
          <div className="filters">
            <div className="popular">
              <h2>Controlar dispositivos</h2>
            </div>
          </div>

          <main>
            <Row>
              {projects.map((project, index) => {
                return (
                  <ProjectCard
                    key={index}
                    {...project}
                    data={devicesDatas[project.title]}
                  />
                );
              })}
            </Row>
          </main>
        </div>
      </div>
      <div className="right">
        <MainRightTopCard rawData={devices} />
        <CardDevices devices={devices} />
       
      </div>
    </div>
  );
}

export default MainContainer;
