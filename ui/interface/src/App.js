import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import React from 'react';
import MainContainer from "./components/MainContainer"
import { ViewDevices } from "./components/ViewDevs";
import { Banner } from "./components/ViewInit";
import IoTControl from './IoTControl';


function App() {
  return (
    <div className="App">
      <Banner/>
      <ViewDevices/>
      
    </div>
  );
}

export default App;
