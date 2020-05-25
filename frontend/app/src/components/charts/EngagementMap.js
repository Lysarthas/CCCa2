import React, { Component } from "react";
import StateEngagementMap from './StateEngagementMap'
import CityEngagementMap from './CityEngagementMap'
import './RightChild.css'

class EngagementMap extends Component {
  constructor(props) {
    super(props);
    this.state = {
      mode: 'state',
      updateFlag: props.updateFlag,
    };
  }

  componentWillReceiveProps(nextProps) {
    this.setState({ updateFlag: nextProps.updateFlag });  
  }

  handler = (ev) => {
    this.setState({
      mode: ev.currentTarget.value
    })
  }

  render() {
    return (
      <div className='parent'>
        {this.state.mode === 'state' ? <StateEngagementMap /> : <CityEngagementMap />}
        <button className="rightchild" value='state' onClick={this.handler}>state mode</button>
        <button className="rightchild" value='city' onClick={this.handler}>city mode</button>
      </div>
    )
  }
}

export default EngagementMap