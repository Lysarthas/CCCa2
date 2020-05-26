import React, { Component } from "react";
import ReactEcharts from "echarts-for-react";
import au_state_json from "./aus_lga_geo.json";
import echarts from "echarts";
import { Spin } from "antd";
import get_db from "../../lib/Pouchdb";

const city_coord_map = {
  Adelaide: "South Australia",
  Brisbane: "Queensland",
  Canberra: "New South Wales",
  Darwin: "Northern Territory",
  "Gold Coast": "Queensland",
  Hobart: "Tasmania",
  Melbourne: "Victoria",
  Newcastle: "New South Wales",
  Perth: "Western Australia",
  "Sunshine Coast": "Queensland",
  Sydney: "New South Wales",
};

class StateEngagementMap extends Component {
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
        left: 'center'
      },
      tooltip: {
        trigger: "item",
        formatter: "{b}<br/>{c} tweets",
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
        min: 800,
        max: 50000,
        text: ["High", "Low"],
        realtime: false,
        calculable: true,
        inRange: {
          color: ["#efefef", "#8cbedc", "#3670ac"],
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
    let res = {};
    for (let i = 0; i < data.length; i++) {
      if (city_coord_map[data[i].key] in res) {
        res[city_coord_map[data[i].key]] += data[i].value;
      } else {
        res[city_coord_map[data[i].key]] = data[i].value;
      }
    }

    let final_res = [];
    for (let state in res) {
      final_res.push({ name: state, value: res[state] });
    }
    return final_res;
  }

  async componentDidMount() {
    echarts.registerMap("Australia", au_state_json);
    const query_option = {
      stale: "update_after",
      reduce: true,
      group_level: 1,
    };
    const history_result = await get_db("history_id_fixed").query(
      "token/covid-tweets-by-location",
      query_option
    );
    this.setState({
      option: this.makeOption(
        "COVID Tweets per capita in the Australia",
        this.convertData(history_result["rows"])
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

export default StateEngagementMap;
