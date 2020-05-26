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
      <Layout style={{height: '100%'}}>
        <Header style={{backgroundColor:'#efefef', marginBottom: '0px', height: '50px'}}>
          <MyHeader />
        </Header>
        <Content style={{height: '100%', flex: 'auto', background: '#e7e7e7'}}>
          <Container />
        </Content>
      </Layout>
    </div>
  );
}

export default App;
