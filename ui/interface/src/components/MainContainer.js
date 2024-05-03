import React from "react";
import "./MainContainer.css";
import Banner from "../assets/img/color-sharp.png";
import Card1 from "../assets/img/img-view3.png";
import Card2 from "../assets/img/img-view3.png";
import Card3 from "../assets/img/img-view3.png";
import Card4 from "../assets/img/img-view3.png";
import Card5 from "../assets/img/img-view3.png";
import Card6 from "../assets/img/img-view3.png";
import MainRightTopCard from "./MainRightTopCard";
import MainRightBottomCard from "./MainRightBottomCard";
import CardDevices from "./CardDevices";
import { Container, Row, Col, Tab, Nav } from "react-bootstrap";
import { ProjectCard } from "./CardView";
import Clock from 'react-live-clock'; // Importando react-live-clock

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
                Horário <Clock format={'dddd, MMMM Do YYYY, h:mm:ss A'} ticking={true} timezone={'America/Sao_Paulo'} />
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
        <MainRightTopCard />
        <CardDevices devices={devices} />
      </div>
    </div>
  );
}

export default MainContainer;