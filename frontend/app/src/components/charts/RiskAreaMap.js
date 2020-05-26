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

class RiskAreaMap extends Component {
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
        formatter: "{b}<br/>admission ratio: {c}",
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
        min: 0.4,
        max: 0.9,
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
    let res = []
    for (let i = 0; i < data.length; i++) {
      const doc = data[i].doc;
      if (Object.values(city_coord_map).includes(doc.place)) {
        res.push({name: doc.place, value: doc.admissions / doc.population});
      }
    }
    return res;
  }

  async componentDidMount() {
    echarts.registerMap("Australia", au_state_json);
    
    const poppulation_result = await get_db('population_data', 'http://shibachan:MuchWOWSuchAmAzE@172.26.131.162:5984/').allDocs({include_docs: true})



    this.setState({
      option: this.makeOption(
        "Hospital admission ratio last year(2019)",
        this.convertData(poppulation_result["rows"])
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

export default RiskAreaMap;
