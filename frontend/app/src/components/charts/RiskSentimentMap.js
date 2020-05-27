// Team members (Team 13):
// Yuansan Liu, 1037351
// Karun Varghese Mathew, 1007247
// Junlin Chen, 1065399
// Jingyi Shao, 1049816
// Han Jiang, 1066425

import React, { Component } from "react";
import RiskAreaMap from "./RiskAreaMap";
import StateSentimentCountMap from "./StateSentimentCountMap";
import "./RightChild.css";
import { ButtonGroup } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import { Button } from "antd";

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
      <div className="parent" style={{ display: "flex", flexDirection: "row" }}>
        <div style={{ width: "80%" }}>
          {this.state.mode === "risk" ? (
            <RiskAreaMap />
          ) : (
            <StateSentimentCountMap />
          )}
        </div>
        <div style={{ width: "20%", marginTop: "10px" }}>
          <ButtonGroup
            vertical
            className="rightchild"
            style={{ marginTop: "10px" }}
          >
            <Button
              value="risk"
              onClick={this.handler}
              style={{ width: "110px", fontSize: '12px', padding: 0}}
            >admission ratio
            </Button>
            <Button
              value="sentiment_count"
              onClick={this.handler}
              style={{ width: "110px", fontSize: '12px', padding: 0 }}
            >
              sentiment count
            </Button>
          </ButtonGroup>
        </div>
      </div>
    );
  }
}

export default RiskSentimentMap;
