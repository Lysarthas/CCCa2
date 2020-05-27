// Team members (Team 13):
// Yuansan Liu, 1037351
// Karun Varghese Mathew, 1007247
// Junlin Chen, 1065399
// Jingyi Shao, 1049816
// Han Jiang, 1066425

import React, { Component } from "react";
import ReactEcharts from "echarts-for-react";
import au_state_json from "./aus_lga_geo.json";
import echarts from "echarts";
import { Spin } from "antd";

const case_map = {
  "New South Wales": [3194, 51],
  "Northern Territory": [29, 0],
  Queensland: [1059, 6],
  "South Australia": [439, 4],
  Tasmania: [228, 13],
  Victoria: [1603, 19],
  "Western Australia": [557, 9],
};

class CaseMap extends Component {
  constructor(props) {
    super(props);
    this.state = {
      option: {},
    };
  }

  makeOption(title, data, min, max) {
    return {
      title: {
        text: title,
        left: "center",
      },
      tooltip: {
        trigger: "item",
        formatter: "{b}<br/>{c} covid cases",
      },
      toolbox: {
        show: true,
        orient: "vertical",
        left: "right",
        top: "center",
        feature: {
          dataView: { readOnly: false },
          restore: {},
          saveAsImage: {},
        },
      },
      visualMap: {
        min: 0,
        max: 3000,
        text: ["High", "Low"],
        realtime: false,
        calculable: true,
        inRange: {
          color: ["#f9d8ba", "#ee8649", "#bc5d32"],
        },
      },
      series: [
        {
          layoutCenter: ["25%", "65%"],
          layoutSize: 900,
          aspectScale: 1.1,
          type: "map",
          mapType: "Australia", // 自定义扩展图表类型
          label: {
            show: false,
          },
          data: data,
        },
      ],
    };
  }

  convertData(data) {
    let res = [];
    for (let state in data) {
      res.push({ name: state, value: data[state][0] });
    }
    return res;
  }

  async componentDidMount() {
    await setTimeout(() => {}, 500);
    echarts.registerMap("Australia", au_state_json);

    this.setState({
      option: this.makeOption(
        "COVID cases in the Australia",
        this.convertData(case_map)
      ),
    });
  }

  render() {
    return (
      <div className="timeline-container">
        {Object.keys(this.state.option).length === 0 ? (
          <Spin size="large" />
        ) : (
          <ReactEcharts option={this.state.option} />
        )}
      </div>
    );
  }
}

export default CaseMap;
