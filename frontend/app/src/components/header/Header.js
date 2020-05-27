// Team members (Team 13):
// Yuansan Liu, 1037351
// Karun Varghese Mathew, 1007247
// Junlin Chen, 1065399
// Jingyi Shao, 1049816
// Han Jiang, 1066425

import React from 'react';
import 'antd/dist/antd.css';
import logo from './logo.png'

function MyHeader() {
  return (
    <div className="header-panel" style={{height: '100%'}}>
      <img src={logo} alt="logo" style={{height: '90%', float: 'left'}}/>
      <h2 style={{position: 'relative', left: '5px', textAlign: 'left'}} >
        COVID-19 Australia Twitter Map
      </h2>
    </div>
  );
}

export default MyHeader;