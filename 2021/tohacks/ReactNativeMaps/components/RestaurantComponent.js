import React from 'react';
import {
  Text,
  View,
  Image,
  Linking,
  TouchableHighlight,
  StyleSheet,
} from 'react-native';
import call from 'react-native-phone-call';
import {RFPercentage} from 'react-native-responsive-fontsize';
import Radar from 'react-native-radar';

import curbside from '../assets/icons/curbside.png';
import mobile_order from '../assets/icons/mobile.png';
import delivery from '../assets/icons/delivery.png';
import phone from '../assets/icons/telephone.png';

import skip_the_dishes from '../assets/icons/skip.png';
import uber_eats from '../assets/icons/uber.png';
import door_dash from '../assets/icons/doordash.png';

import bike from "../assets/icons/bike.png"
import car from "../assets/icons/car.png"

export default class ActiveRestaurantComponent extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      expanded: false,
      bike: false,
      car: false,
      walking: false,
      distance: false,
    };

    this.placePhoneCall = this.placePhoneCall.bind(this);
    this.getDirections = this.getDirections.bind(this);
    this.getDelivery = this.getDelivery.bind(this);
    this.placeOrder = this.placeOrder.bind(this);
    this.toggleExpand = this.toggleExpand.bind(this);
  }

  placePhoneCall(val) {
    var args = {number: val, prompt: true};
    call(args).catch(console.error);
  }

  getDirections() {
    Radar.getLocation()
      .then(loc => {
        var user_loc = {
          latitude: loc.location.latitude,
          longitude: loc.location.longitude,
        };
        Radar.getDistance({
          origin: user_loc,
          destination: {
            longitude: parseFloat(this.props.restaurant.Longitude),
            latitude: parseFloat(this.props.restaurant.Latitude),
          },
          modes: ["bike", "car"],
          units: 'metric',
        })
          .then(result => {
            console.log(result);

            this.setState({bike: result.routes.bike.duration.text, car: result.routes.car.duration.text, distance: result.routes.car.distance.text})
            // do something with result.routes
          })
          .catch(err => {
              console.log(err)
            // optionally, do something with err
          });
      })
      .catch(err => {
        console.log(err);
      });
  }

  getDelivery() {
    console.log('Delivery');
  }

  placeOrder(url) {
    console.log(url);
    Linking.openURL(url);
  }

  toggleExpand() {
    console.log('Toggling expand');
    this.setState({expanded: !this.state.expanded});
  }

  render() {
    return (
      <View style={styles.main_container}>
        <View style={{flexDirection: 'row'}}>
          <Text style={styles.restaurant_name}>
            {this.props.restaurant.name}
          </Text>
          <Text
            style={{paddingTop: 10, paddingRight: 5}}
            onPress={this.toggleExpand}>
            Expand
          </Text>
        </View>

        <Text style={styles.restaurant_description}>
          {this.props.restaurant.description}
        </Text>

        {parseBool(this.props.restaurant['Curbside Pickup']) === true && (
          <View style={styles.inline}>
            <Image source={curbside} style={styles.icon} />
            <Text
              style={{
                flex: 1,
                fontSize: RFPercentage(1.5),
                fontWeight: 'bold',
                color: '#009353',
                paddingLeft: 10,
              }}>{`Curbside\nPickup`}</Text>
            <TouchableHighlight
              style={{
                borderRadius: 20,
                backgroundColor: '#FF7A7A',
                padding: 7,
                zIndex: 3,
                elevate: 3,
              }}
              onPress={this.getDirections}
              underlayColor="blue">
              <Text style={{color: 'white', fontSize: RFPercentage(2)}}>
                Take me there
              </Text>
            </TouchableHighlight>
          </View>
        )}
        {parseInt(this.props.restaurant['In-House Delivery']) === true && (
          <View>
            <Image source={delivery} style={styles.icon} />
            <Text>{`Delivery`}</Text>
            <TouchableHighlight
              style={{borderRadius: 30}}
              onPress={this.getDelivery}>
              <Text style={{padding: 20}}>Order Online</Text>
            </TouchableHighlight>
          </View>
        )}

        {parseInt(this.props.restaurant.url) === true && (
          <View>
            <Image source={mobile_order} style={styles.icon} />
            <Text>{`Mobile\nOrder`}</Text>
            <TouchableHighlight
              style={{borderRadius: 30}}
              onPress={() => this.placeOrder(this.props.restaurant.url)}>
              <Text style={{padding: 20}}>Order Online</Text>
            </TouchableHighlight>
          </View>
        )}

        <View style={styles.inline}>
          {this.props.restaurant.SkipTheDishes !== '' && (
            <TouchableHighlight
              onPress={() =>
                this.placeOrder(this.props.restaurant.SkipTheDishes)
              }>
              <Image
                source={skip_the_dishes}
                style={styles.icon}
                value={this.props.restaurant.SkipTheDishes}
              />
            </TouchableHighlight>
          )}
          {this.props.restaurant.DoorDash !== '' && (
            <TouchableHighlight
              onPress={() => this.placeOrder(this.props.restaurant.DoorDash)}>
              <Image
                source={door_dash}
                style={styles.icon}
                value={this.props.restaurant.DoorDash}
              />
            </TouchableHighlight>
          )}
          {this.props.restaurant.UberEats !== '' && (
            <TouchableHighlight
              onPress={() => this.placeOrder(this.props.restaurant.UberEats)}>
              <Image
                source={uber_eats}
                style={styles.icon}
                value={this.props.restaurant.UberEats}
              />
            </TouchableHighlight>
          )}

          {parseInt(this.props.restaurant.phone.split('.').join('')) !==
            NaN && (
            <TouchableHighlight
              onPress={() =>
                this.placePhoneCall(
                  this.props.restaurant.phone.split('.').join(''),
                )
              }>
              <Image source={phone} style={styles.icon} />
            </TouchableHighlight>
          )}
        </View>

        <View>
            <Text style={{paddingBottom: 20}}>You are {this.state.distance} away which is:</Text>
            <View>
            <View style={styles.inline_distance}>
                <Text>{this.state.bike}</Text>
                <Image source={bike} style={styles.icon} />
            </View>

            <View style={styles.inline_distance}>
                <Text >{this.state.car}</Text>
                <Image source={car} style={styles.icon} />
            </View>
            </View>
        </View>
      </View>
    );
  }
}

function parseBool(val) {
  return val === true || val === 'true' || val === 'TRUE';
}

const styles = StyleSheet.create({
  fill_container: {
    flex: 1,
  },

  icon: {
    height: 40,
    width: 40,
    resizeMode: 'contain',
    flex: 1,
  },

  main_container: {
    flex: 1,
    backgroundColor: 'white',
    flexDirection: 'column',
    padding: 20,
  },

  restaurant_name: {
    flex: 1,
    fontSize: RFPercentage(4),
    padding: 5,
  },

  restaurant_description: {
    flex: 1,
    padding: 5,
    paddingBottom: 20,
  },

  inline: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-around',
    paddingBottom: 15,
  },

  inline_distance: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingBottom: 15,
  },
});
