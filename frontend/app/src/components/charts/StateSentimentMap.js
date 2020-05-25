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
      updateFlag: props.updateFlag,
    };
  }

  componentWillReceiveProps(nextProps) {
    this.setState({ updateFlag: nextProps.updateFlag });  
  }


  makeOption(title, data, min, max) {
    return {
      title: {
        text: title,
        left: 'center'
      },
      tooltip: {
        trigger: "item",
        formatter: "{b}<br/>mean sentiments score: {c}",
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
        min: 0.3,
        max: 0.8,
        precision: 0.01,
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
    let res = {};
    for (let i = 0; i < data.length; i++) {
      const stats = data[i].value;
      const statObj = {sum: stats.sum, count: stats.count}
      if (city_coord_map[data[i].key] in res) {
        res[city_coord_map[data[i].key]].push(statObj);
      } else {
        res[city_coord_map[data[i].key]] = [statObj];
      }
    }

    let final_res = [];
    for (let state in res) {
      let count = 0;
      let sum = 0;
      for (let i = 0; i < res[state].length; i++) {
        count += res[state][i].count;
        sum += res[state][i].sum;
      }
      final_res.push({ name: state, value: sum/count });
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
    const current_result = await get_db('twitter_sentiments_1', 'http://shibachan:MuchWOWSuchAmAzE@172.26.131.132:5984/').query('sentiments/locations_neg_stats', query_option);
    const history_result = await get_db('twitter_sentiments_2', 'http://shibachan:MuchWOWSuchAmAzE@172.26.131.132:5984/').query('MuchWOWSuchAmAzE/locations_neg_stats', query_option);
    const rows = history_result['rows'].concat(current_result['rows'])

    this.setState({
      option: this.makeOption(
        "Sentiments in the Australia",
        this.convertData(rows)
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
