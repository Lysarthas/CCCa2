import React, { Component } from "react";
import EngagementTimeline from "../charts/EngagementTimeline";
import SentimentTimeline from "../charts/SentimentTimeline";
import EngagementMap from '../charts/EngagementMap'
import StateSentimentMap from '../charts/StateSentimentMap'
import CaseMap from '../charts/CaseMap';
import { Row, Col, Button } from "antd";
import StateTopics from '../charts/StateTopics';
import RiskSentimentMap from '../charts/RiskSentimentMap'
import CaseTimeline from '../charts/CaseTimline';

class Container extends Component {
  constructor(props) {
    super(props);
    this.state = {
      timeline: 0,
      geomap: 0,
      updateFlag: false,
    };
  }

  sections = {
    timeline: {
      titles: ["Engagement", "Sentiment", "Cases"],
      defaultIndex: 0,
      components: [EngagementTimeline, SentimentTimeline, CaseTimeline],
    },
    geomap: {
      titles: ["Engagement", "Sentiment", "Covid Cases"],
      defaultIndex: 0,
      components: [EngagementMap, StateSentimentMap, CaseMap]
    }
  };

  handler(section_name, index) {
    if (index === this.state[section_name]) {
      return;
    }

    let newState = {};
    newState[section_name] = index;
    newState['updateFlag'] = !this.state.updateFlag
    this.setState(newState);
  }

  createSection = (section_name, index) => {
    const Section = this.sections[section_name].components[index];
    return <Section updateFlag={this.state.updateFlag}/>;
  };

  render() {
    return (
      <div className="dashboard">
        <Row>
          {Object.keys(this.sections).map((section) => (
            <Col span={11} key={section} style={{height: '340px', backgroundColor: 'white', margin: '20px'}}>
              {this.createSection(section, this.state[section])}
              {[...Array(this.sections[section].titles.length).keys()].map((index) => (
                <Button
                  size='small'
                  key={index}
                  onClick={() => this.handler(section, index)}
                >
                  {this.sections[section].titles[index]}
                </Button>
              ))}
            </Col>
            
          ))}
          <Col span={11} key='risk-areas-map' style={{height: '320px', backgroundColor: 'white', margin: '20px'}}>
            <RiskSentimentMap />
          </Col>
          <Col span={11} key='topics' style={{height: '320px', backgroundColor: 'white', margin: '20px'}}>
            <StateTopics />
          </Col>
        </Row>
      </div>
    );
  }
}

export default Container;
