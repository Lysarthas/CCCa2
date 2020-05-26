import React, {Component} from 'react';
import get_db from '../../lib/Pouchdb'
import ReactEcharts from 'echarts-for-react';
import {Spin} from 'antd';

class SentimentTimeline extends Component {
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
        text: 'Neg Sentiments score',
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

  // mergeData(current_result, history_result) {
  //   let dates = []
  //   let res = []
  //   current_result = current_result['rows']
  //   history_result = history_result['rows']
  //   for (let i = 0; i < current_result; i++) {
  //     if (!dates.includes(current_result[i].key)) {
  //       dates.push(current_result);
  //       res.push(current_result[i])
  //     }
  //   }
  // }

  async componentDidMount() {
    let mean_score = []
    let x_axies = []
    let query_option = {
      stale: 'update_after',
      reduce: true,
      group_level: 2
    }

    const current_result = await get_db('twitter_sentiments_1', 'http://shibachan:MuchWOWSuchAmAzE@172.26.131.132:5984/').query('sentiments/timeline_neg_stats', query_option);
    const history_result = await get_db('twitter_sentiments_2', 'http://shibachan:MuchWOWSuchAmAzE@172.26.131.132:5984/').query('MuchWOWSuchAmAzE/timeline_neg_stats', query_option);
    const rows = history_result['rows'].concat(current_result['rows'])

    for (let i = 0; i < rows.length; i++) {
      const stats = rows[i].value;
      mean_score.push(stats.sum / stats.count);
      x_axies.push((rows[i].key[0] + 1).toString() + '/' + rows[i].key[1])
    }

    this.setState({
      option: this.makeOption(x_axies, mean_score)
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

export default SentimentTimeline;