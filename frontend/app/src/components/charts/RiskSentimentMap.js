import React, { Component } from "react";
import RiskAreaMap from "./RiskAreaMap";
import StateSentimentCountMap from "./StateSentimentCountMap";
import "./RightChild.css";
import {ButtonGroup, Button} from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import { Row, Col } from "antd";

class RiskSentimentMap extends Component {
  constructor(props) {
    super(props);
    this.state = {
      mode: "risk",
      updateFlag: props.updateFlag,
    };
  }

  componentWillReceiveProps(nextProps) {
    this.setState({ updateFlag: nextProps.updateFlag });
  }

  handler = (ev) => {
    this.setState({
      mode: ev.currentTarget.value,
    });
  };

  render() {
    return (
      <div className="parent">
        <Row>
          <Col span={23}>
            {this.state.mode === "risk" ? (
              <RiskAreaMap />
            ) : (
              <StateSentimentCountMap />
            )}
          </Col>
          <Col span={1}>
            <ButtonGroup vertical className="rightchild" style={{marginTop: '60px', marginLeft: '10px', width: '70px'}}>
              <Button value="risk" 
                onClick={this.handler} 
                variant="light"
                style={{margin: '2px'}}>
                admis-<br/>sion<br/>ratio
              </Button>
              <Button value="sentiment_count" 
              onClick={this.handler} 
              variant="light"
              style={{margin: '2px'}}>
                senti-<br/>ment<br/>count
              </Button>
            </ButtonGroup>
          </Col>
        </Row>
      </div>
    );
  }
}

export default RiskSentimentMap;
