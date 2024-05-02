import { Col, Tab, Nav } from "react-bootstrap";
import TrackVisibility from 'react-on-screen';

export const ProjectCard = ({ title, description, imgUrl, data }) => {
  const handleCommand = async (command) => {
    try {
      const response = await fetch(`http://192.168.0.181:5001/devices/${title}/command`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ command })
      });
      const responseData = await response.json();
      console.log(responseData);
    } catch (error) {
      console.error('Error sending command:', error);
    }
  };

  return (
    <Col size={12} sm={6} md={4}>
      <div className="proj-imgbx">
        <img src={imgUrl} alt="Project" />
        <div className="proj-txtx">
          <h4>{title}</h4>
          <span>{description}</span>
        </div>
        <div className="overlay">
          
          <div className="large-text">
          {data} °C
          </div>
        </div>

        <div className="tab-container">
          <TrackVisibility>
            {({ isVisible }) =>
              <div className={isVisible ? "animate__animated animate__fadeIn": ""}>
                <Tab.Container id="projects-tabs" defaultActiveKey="first">
                  <Nav variant="pills" className="nav-pills mb-5 justify-content-center align-items-center" id="pills-tab" style={{ position: 'absolute', bottom: '-40px', left: '50%', transform: 'translateX(-50%)' }}>
                    <Nav.Item>
                      <Nav.Link eventKey="first" onClick={() => handleCommand('turn_on')}style={{ fontSize: '12px' }}>on</Nav.Link>
                    </Nav.Item>
                    <Nav.Item>
                      <Nav.Link eventKey="second" onClick={() => handleCommand('turn_off')}style={{ fontSize: '12px' }}>off</Nav.Link>
                    </Nav.Item>
                    <Nav.Item>
                      <Nav.Link eventKey="third" onClick={() => handleCommand('restart')}style={{ fontSize: '12px' }}>restart</Nav.Link>
                    </Nav.Item>
                  </Nav>
                </Tab.Container>
              </div>
            }
          </TrackVisibility>
        </div>
      </div>
    </Col>
  );
};
