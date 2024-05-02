
import { useState } from "react";
import { Col, Row, Alert } from "react-bootstrap";

export const DeviceName= ({ deviceName, onSubmit }) => {
  const [newName, setNewName] = useState('');
  const [status, setStatus] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`http://192.168.0.181:5001/devices/${deviceName}/name`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ new_name: newName })
      });

      const data = await response.json();

      if (response.ok) {
        setStatus('success');
        setMessage(data.message);
        onSubmit();
      } else {
        setStatus('error');
        setMessage(data.error);
      }
    } catch (error) {
      setStatus('error');
      setMessage('An error occurred');
    }
  }

  return (
    <div className="newsletter-bx wow slideInUp">
      <Row>
        <Col lg={12} md={6} xl={5}>
          <h3>Novo nome:</h3>
        </Col>
      </Row>
      <Row>
        <Col md={6} xl={7}>
          <form onSubmit={handleSubmit}>
            <div className="new-email-bx">
              <input value={newName} type="text" onChange={(e) => setNewName(e.target.value)} placeholder="New Device Name" />
              <button type="submit">Submit</button>
            </div>
          </form>
        </Col>
      </Row>
        {status === 'sending' && <Alert>Sending...</Alert>}
        {status === 'error' && <Alert variant="danger">{message}</Alert>}
        {status === 'success' && <Alert variant="success">{message}</Alert>}
    </div>

    
  );
};