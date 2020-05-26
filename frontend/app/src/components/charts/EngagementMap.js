import React, { Component } from "react";
import StateEngagementMap from "./StateEngagementMap";
import CityEngagementMap from "./CityEngagementMap";
import "./RightChild.css";
import { ButtonGroup } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import { Button } from "antd";

class EngagementMap extends Component {
  constructor(props) {
    super(props);
    this.state = {
      mode: "state",
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
      <div className="parent" style={{display: 'flex', flexDirection: 'row'}}>
        <div style={{width:'80%'}}>
          {this.state.mode === "state" ? (
            <StateEngagementMap />
          ) : (
            <CityEngagementMap />
          )}
        </div>
        <div style={{width:'20%', marginTop: '10px'}}>
          <ButtonGroup
            vertical
            style={{ marginTop: '10px'}}
          >
            <Button
              value="state"
              style={{ width: "100px" }}
              onClick={this.handler}
            >
              state mode
            </Button>
            <Button value="city" style={{ width: "100px" }} onClick={this.handler}>
              city mode
            </Button>
          </ButtonGroup>
        </div>
      </div>
    );
  }
}

export default EngagementMap;
