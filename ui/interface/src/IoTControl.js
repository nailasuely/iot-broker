import React, { useState, useEffect } from 'react';

const IoTControl = () => {
    const [deviceData, setDeviceData] = useState('');
    const [command, setCommand] = useState('');

    const fetchData = async () => {
        try {
            const response = await fetch('http://192.168.0.181:5001/devices/TemperatureSensor/data');
            const data = await response.json();
            
            if (response.ok) {
                setDeviceData(data.data);
            } else {
                console.error('Failed to fetch data:', data.error);
            }
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    };

    const sendCommand = async () => {
        try {
            const response = await fetch('http://192.168.0.181:5001/devices/TemperatureSensor/command', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ command }),
            });
            if (response.ok) {
                console.log(`Command '${command}' sent successfully`);
            } else {
                const errorData = await response.json();
                console.error('Failed to send command:', errorData.error);
            }
        } catch (error) {
            console.error('Error sending command:', error);
        }
    };

    useEffect(() => {
        const fetchDataInterval = setInterval(fetchData, 1000);
        
        return () => clearInterval(fetchDataInterval);
    }, []);

    return (
        <div>
            <h2>IoT Device Control</h2>
            <p>Device Data: {deviceData}</p>
            <input type="text" value={command} onChange={(e) => setCommand(e.target.value)} />
            <button onClick={sendCommand}>Send Command</button>
        </div>
    );
};

export default IoTControl;
