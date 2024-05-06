import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import React from 'react';
import { ViewDevices } from "./components/ViewDevs";
import { Banner } from "./components/ViewInit";


function App() {
  return (
    <div className="App">
      <Banner/>
      <ViewDevices/> 
    </div>
  );
}

export default App;
