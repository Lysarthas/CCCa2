// Team members (Team 13):
// Yuansan Liu, 1037351
// Karun Varghese Mathew, 1007247
// Junlin Chen, 1065399
// Jingyi Shao, 1049816
// Han Jiang, 1066425

import React, {Component} from 'react';
import get_db from '../../lib/Pouchdb'
import ReactEcharts from 'echarts-for-react';
import {Spin} from 'antd';

class EngagementTimeline extends Component {
  constructor(props) {
    super(props);
    this.state = {
      option: {},
      updateFlag: props.updateFlag,
    };
  }

  makeOption(x_axies, y) {
    return {
      tooltip: {},
      title: {
        text: 'COVID Tweets timeline',
        left: 'center'
      },
      xAxis: {
        type: 'category',
        data: x_axies,
      },
      yAxis: {
          type: 'value'
      },
      series: [{
          data: y,
          type: 'line',
          symbol: 'circle',
          symbolSize: 10,
          areaStyle: {},
          lineStyle: {
              width: 1.5,
              color: '#00a9e6'
          },
          itemStyle: {
              borderWidth: 2,
              color: '#00a9e6'
          }
      }]
    }
  }

  componentWillReceiveProps(nextProps) {
    this.setState({ updateFlag: nextProps.updateFlag });  
  }

  async componentDidMount() {
    let tweet_count = []
    let x_axies = []
    let query_option = {
      stale: 'update_after',
      reduce: true,
      group_level: 2
    }

    const history_result = await get_db('history_id_fixed').query('token/covid_timeline_count_all', query_option);
    // const current_result = await get_db('junlin_id_fixed').query('token/covid_timeline_count_all', query_option);

    let rows = history_result.rows;
    for (let i = 0; i < rows.length; i++) {
      tweet_count.push(rows[i].value);
      x_axies.push((rows[i].key[0] + 1).toString() + '/' + rows[i].key[1])
    }

    this.setState({
      option: this.makeOption(x_axies, tweet_count)
    })
  }

  render() {
    return (
      <div className="timeline-container">
        {Object.keys(this.state.option).length === 0 ? <Spin size="large"/> : 
          <ReactEcharts
            option={this.state.option}
          />
        }
      </div>
    )
  }

}

export default EngagementTimeline;