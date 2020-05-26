import React from 'react';
import { PageHeader } from 'antd';
import 'antd/dist/antd.css';

function MyHeader() {
  return (
    <div className="header-panel" style={{height: '100%'}}>
      <PageHeader
        className="site-page-header"
        title="COVID-19 Australia Twitter Map"
        subTitle="by CCCp2"
        style={{height: '100%'}}
      />
    </div>
  );
}

export default MyHeader;