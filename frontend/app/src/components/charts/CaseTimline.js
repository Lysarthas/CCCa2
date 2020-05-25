import React, {Component} from 'react';
import get_db from '../../lib/Pouchdb'
import ReactEcharts from 'echarts-for-react';
import {Spin} from 'antd';


const case_timeline = [{'1/25': 3},
{'1/26': 4},
{'1/27': 5},
{'1/28': 5},
{'1/29': 7},
{'1/30': 9},
{'1/31': 9},
{'2/1': 12},
{'2/2': 12},
{'2/3': 12},
{'2/4': 13},
{'2/5': 14},
{'2/6': 15},
{'2/7': 15},
{'2/8': 15},
{'2/9': 15},
{'2/10': 15},
{'2/11': 15},
{'2/12': 15},
{'2/13': 15},
{'2/14': 15},
{'2/15': 15},
{'2/16': 15},
{'2/17': 15},
{'2/18': 15},
{'2/19': 15},
{'2/20': 15},
{'2/21': 17},
{'2/22': 21},
{'2/23': 22},
{'2/24': 22},
{'2/25': 23},
{'2/26': 23},
{'2/27': 23},
{'2/28': 23},
{'2/29': 25},
{'3/1': 27},
{'3/2': 33},
{'3/3': 33},
{'3/4': 33},
{'3/5': 57},
{'3/6': 62},
{'3/7': 70},
{'3/8': 77},
{'3/9': 92},
{'3/10': 92},
{'3/11': 122},
{'3/12': 140},
{'3/13': 189},
{'3/14': 197},
{'3/15': 298},
{'3/16': 336},
{'3/17': 414},
{'3/18': 510},
{'3/19': 709},
{'3/20': 873},
{'3/21': 1081},
{'3/22': 1098},
{'3/23': 1709},
{'3/24': 2136},
{'3/25': 2423},
{'3/26': 2799},
{'3/27': 2985},
{'3/28': 3635},
{'3/29': 3966},
{'3/30': 4245},
{'3/31': 4557},
{'4/1': 4860},
{'4/2': 4976},
{'4/3': 5350},
{'4/4': 5454},
{'4/5': 5635},
{'4/6': 5795},
{'4/7': 5844},
{'4/8': 5956},
{'4/9': 6052},
{'4/10': 6152},
{'4/11': 6289},
{'4/12': 6313},
{'4/13': 6322},
{'4/14': 6366},
{'4/15': 6416},
{'4/16': 6458},
{'4/17': 6468},
{'4/18': 6533},
{'4/19': 6606},
{'4/20': 6612},
{'4/21': 6625},
{'4/22': 6647},
{'4/23': 6661},
{'4/24': 6667},
{'4/25': 6687},
{'4/26': 6703},
{'4/27': 6713},
{'4/28': 6725},
{'4/29': 6738},
{'4/30': 6746},
{'5/1': 6762},
{'5/2': 6767},
{'5/3': 6783},
{'5/4': 6801},
{'5/5': 6825},
{'5/6': 6849},
{'5/7': 6875},
{'5/8': 6896},
{'5/9': 6914},
{'5/10': 6929},
{'5/11': 6941},
{'5/12': 6948},
{'5/13': 6964},
{'5/14': 6975},
{'5/15': 6989},
{'5/16': 7019},
{'5/17': 7036},
{'5/18': 7045},
{'5/19': 7060},
{'5/20': 7068},
{'5/21': 7079},
{'5/22': 7081},
{'5/23': 7095},
{'5/24': 7106},
{'5/25': 7109}]

class CaseTimeline extends Component {
  constructor(props) {
    super(props);
    this.state = {
      option: {},
      updateFlag: props.updateFlag,
    };
  }

  makeOption(x_axies, y) {
    let series = []
    let legend = []
    for (let i = 0; i < x_axies.length; i++) {
      legend.push(y[i].name);
      series.push({
        name: y[i].name,
        data: y[i].data,
        type: 'line',
        symbol: 'circle',
        symbolSize: 10,
        areaStyle: {
          color: y[i].color
        },
        lineStyle: {
            width: 1.5,
            color: y[i].color
        },
        xAxisIndex: y[i].xAxisIndex,
        itemStyle: {
            borderWidth: 2,
            color: y[i].color
        }
      })
    }
    
    return {
      tooltip: {},
      title: {
        text: 'COVID cumulative cases timeline vs tweets engagement',
        left: 'center'
      },
      legend: {
        top: '90%',
        data:legend
      },
      xAxis: x_axies,
      yAxis: {
          type: 'value'
      },
      series: series
    }
  }

  componentWillReceiveProps(nextProps) {
    this.setState({ updateFlag: nextProps.updateFlag });  
  }

  async componentDidMount() {
    let num_new_cases = []
    let x_axies_0 = []
    
    for (let i = 0; i < case_timeline.length; i++) { 
      x_axies_0.push(Object.keys(case_timeline[i])[0]);
      num_new_cases.push(Object.values(case_timeline[i])[0]);
    }

    let query_option = {
      stale: 'update_after',
      reduce: true,
      group_level: 2
    }
    const history_result = await get_db('history_id_fixed').query('token/covid_timeline_count_all', query_option);
    let rows = history_result.rows;
    let x_axies_1 = []
    let tweet_count = []
    for (let i = 0; i < rows.length; i++) {
      tweet_count.push(rows[i].value);
      x_axies_1.push((rows[i].key[0] + 1).toString() + '/' + rows[i].key[1])
    }

    const x_axies = [{
      type: 'category',
      data: x_axies_0,
    }, {
      type: 'category',
      data: x_axies_1
    }]

    const y = [{
      data: num_new_cases,
      xAxisIndex: 0,
      name: 'cumulative cases',
      color: '#5793f3'
    }, {
      data: tweet_count,
      xAxisIndex: 1,
      name: 'tweets engagement',
      color: '#d14a61'
    }]

    this.setState({
      option: this.makeOption(x_axies, y)
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

export default CaseTimeline;