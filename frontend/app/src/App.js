import React from 'react';
import './App.css';
import MyHeader from './components/header/Header';
import Container from './components/container/Container'
import 'antd/dist/antd.css';
import { Layout } from 'antd';

const { Header, Content } = Layout;

function App() {
  return (
    <div className="App">
      <Layout style={{height: '100%', backgroundColor: '#e7e7e7'}}>
        <Header style={{backgroundColor:'#efefef', height: '50px'}}>
          <MyHeader />
        </Header>
        <Content style={{background: '#e7e7e7'}}>
          <Container />
        </Content>
      </Layout>
    </div>
  );
}

export default App;
