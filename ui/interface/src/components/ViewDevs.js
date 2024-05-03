import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Tab, Nav } from "react-bootstrap";
import { ProjectCard } from "./CardView";
import projImg1 from "../assets/img/img-view3.png";
import colorSharp2 from "../assets/img/color-sharp2.png";
import 'animate.css';
import TrackVisibility from 'react-on-screen';
import MainContainer from "./MainContainer";
import Contain from "./Container";
import { IP } from "./IP";



export const ViewDevices = () => {
  const [deviceData, setDeviceData] = useState({});
  const [rawData, setRawData] = useState([]);
  const [projects, setProjects] = useState([]);
  const [devices, setDevices] = useState([]);
  console.log(deviceData)

  const fetchDevices = async () => {
    try {
      const response = await fetch(`http://${IP}:5001/devices`);
      const devices = await response.json();
      const availableDevices = devices.slice(0, 6); // Limita a 6 dispositivos, dps melhorar isso
      const deviceProjects = availableDevices.map(device => ({
        title: device,
        imgUrl: projImg1,
        data: ''
      }));
      // Preenche os projetos restantes com 'Não conectado'
      while (deviceProjects.length < 6) {
        deviceProjects.push({
          title: 'Não conectado',
          imgUrl: projImg1,
          data: ''
        });
      }
      setProjects(deviceProjects);
      setDevices(devices)
    } catch (error) {
      console.error('Error fetching devices:', error);
    }
  };

  const fetchData = async (deviceName) => {
    try {
      if (deviceName !== 'Não conectado') { // Verifica se o nome do dispositivo é diferente de 'Não conectado'
        const response = await fetch(`http://${IP}:5001/devices/${deviceName}/data`);
        console.log((response))
        const responseData = await response.json();
        if (response.ok) {
          if (responseData.data && responseData.data.data) { // Verifica se responseData.data e responseData.data.data não são undefined
            // Adicionar os dados brutos ao histórico de dados brutos
            addToRawData(responseData.data);
    
            // Armazenar apenas o campo "data" em deviceData
            setDeviceData(prevState => {
              const newData = responseData.data.data;
              return {
                ...prevState,
                [deviceName]: newData
              };
            });
          } else {
            console.error(`Invalid data received for ${deviceName}:`, responseData);
          }
        } else {
          console.error(`Failed to fetch data for ${deviceName}:`, responseData.error);
        }
      } else {
        console.error(`Device is not connected: ${deviceName}`);
      }
    } catch (error) {
      console.error(`Error fetching data for ${deviceName}:`, error);
    }
  };
  

  // Função para adicionar dados ao histórico de dados 
  const addToRawData = (data) => {
    setRawData(prevState => {
      const newData = [...prevState, data];
      return newData.slice(-10); 
    });
  };

  useEffect(() => {
    fetchDevices();
  }, []);

 /* useEffect(() => {
    const fetchDataInterval = setInterval(() => {
      projects.forEach(project => {
        fetchData(project.title);
      });
    }, 1000);
    return () => clearInterval(fetchDataInterval);
  }, [projects]);*/
  

  useEffect(() => {
    const fetchDataInterval = setInterval(() => {
      fetchDevices();
      projects.forEach(project => {
        fetchData(project.title);
      });
    }, 1000);
    return () => clearInterval(fetchDataInterval);
  }, [projects]);

  return (    
    <section className="project" id="projects">
      <Container>
        <Row>
          <Col size={12}>
            <TrackVisibility>
              {({ isVisible }) =>
              <div className={isVisible ? "animate__animated animate__fadeIn": ""}>
                <h2>Dispositivos</h2>
                <Tab.Container id="projects-tabs" defaultActiveKey="first">
                  <Nav variant="pills" className="nav-pills mb-5 justify-content-center align-items-center" id="pills-tab">
                    <Nav.Item>
                      <Nav.Link eventKey="first">DashBoard</Nav.Link>
                    </Nav.Item>
                    <Nav.Item>
                      <Nav.Link eventKey="second">View</Nav.Link>
                    </Nav.Item>
                  </Nav>
                  <Tab.Content id="slideInUp" className={isVisible ? "animate__animated animate__slideInUp" : ""}>
                    <Tab.Pane eventKey="first">
                      <Row>
                        {
                          <Contain datas={rawData} devices={devices} projects={projects} devicesDatas={deviceData}/>
                        }
                      </Row>
                    </Tab.Pane>
                    <Tab.Pane eventKey="second">
                    <Row>
                       {
                          projects.map((project, index) => {
                            return (
                              <ProjectCard
                                key={index}
                                {...project}
                                data={deviceData[project.title]}
                                />
                            )
                          })
                        }
                      </Row>
                    </Tab.Pane>
                  </Tab.Content>
                </Tab.Container>
              </div>}
            </TrackVisibility>
          </Col>
        </Row>
      </Container>
      <img className="background-image-right" src={colorSharp2} alt="background"></img>
    </section>
  );
};


