// Team members (Team 13):
// Yuansan Liu, 1037351
// Karun Varghese Mathew, 1007247
// Junlin Chen, 1065399
// Jingyi Shao, 1049816
// Han Jiang, 1066425

import React, { Component } from "react";
import get_db from "../../lib/Pouchdb";
import { Map, TileLayer, CircleMarker} from 'react-leaflet'

const city_coord_map = {
  Adelaide: [138.6, -34.93],
  Brisbane: [53.02, -27.46],
  Canberra: [149.13, -35.31],
  Darwin: [130.85, -12.43],
  "Gold Coast": [153.44, -28.07],
  Hobart: [147.29, -42.85],
  Melbourne: [144.96, -37.81],
  Newcastle: [151.75, -32.92],
  Perth: [115.84, -31.96],
  "Sunshine Coast": [152.56, -25.88],
  Sydney: [151.21, -33.87],
};


class CityEngagementMap extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: [],
      lat: -27.115821,
      lng: 134.952667,
      zoom: 4,
    };
  }


  drawcCircle(data) {
    let coord = city_coord_map[data.key]
    let latlng = {lat: coord[1], lng: coord[0]}
    let radius = Math.min(data.value / 500, 20)
    return (
      <CircleMarker 
        key={data.key} 
        center={latlng} 
        radius={radius} 
        fillOpacity={0.7}
        fillColor='purple'
        color='purple'
      />
    )
  }

  async componentDidMount() {
    const query_option = {
      stale: "update_after",
      reduce: true,
      group_level: 1,
    };
    const history_result = await get_db("history_id_fixed").query(
      "token/covid-tweets-by-location",
      query_option
    );
    
    this.setState({data: history_result['rows']})
    
  }

  render() {
    const position = [this.state.lat, this.state.lng]
    const bound = [[-45.134095, 109.041799], [-11.585642, 153.162890]];
    return (
      <div className="Geo-container" >
        <Map center={position} zoom={this.state.zoom} style={{height:'300px'}} boundsOptions={bound}>
          <TileLayer
            attribution='&copy; <a href="https://stadiamaps.com/">Stadia Maps</a>, &copy; <a href="https://openmaptiles.org/">OpenMapTiles</a> &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'
            url="https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png" />
          {
            this.state.data.map(city => this.drawcCircle(city))
          }
        </Map>
      </div>
    );
  }
}

export default CityEngagementMap;
