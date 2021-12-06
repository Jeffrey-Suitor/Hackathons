/*This is an Example of React Native Map*/
import React from 'react';
import {View, TouchableOpacity, Image, StyleSheet} from 'react-native';
import MapView, {Marker} from 'react-native-maps';
import Radar from 'react-native-radar';
import my_map_style from './assets/map/map_style.json';
import {SearchBar} from 'react-native-elements';
import RestaurantComponent from './components/RestaurantComponent';
import CheckRestaurantVisible from './components/CheckRestaurantVisible';

import restaurant_data from './data/restaurants.json';

import center_button_icon from './assets/icons/location.png';
import search_icon from './assets/icons/search.png';

import inactive_arrow from './assets/icons/tag_inactive.png';
import active_arrow from './assets/icons/tag_active.png';
import ActiveRestaurantComponent from './components/RestaurantComponent';

export default class App extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      search: '',
      region: {
        latitude: 37.78825,
        longitude: -122.4324,
        latitudeDelta: 0.05,
        longitudeDelta: 0.05,
      },
      visible_count: 0,
      search_active: false,
      active_restaurant: false,
    };

    this.onRegionChangeComplete = this.onRegionChangeComplete.bind(this);
    this.updateSearch = this.updateSearch.bind(this);
    this.get_user_location = this.get_user_location.bind(this);
    this.activateRestaurant = this.activateRestaurant.bind(this);
    this.deactivateRestaurant = this.deactivateRestaurant.bind(this);
    Radar.requestPermissions(true);
    this.get_user_location();
  }

  async get_user_location() {
    await Radar.getLocation()
      .then(loc => {
        var temp_region = {
          latitude: loc.location.latitude,
          longitude: loc.location.longitude,
          latitudeDelta: 0.03,
          longitudeDelta: 0.03,
        };
        this.setState({region: temp_region});
      })
      .catch(err => {
        console.log(err);
      });
  }

  onRegionChangeComplete(event) {
    this.setState({visible_count: 0});
    this.setState({region: event});
  }

  // pass tag to function, return list of relevant restaurants
  updateSearch(event) {
    console.log(event);
    if (event === '') {
      this.setState({search: event, search_active: false});
      this.deactivateRestaurant();
    } else {
      this.setState({search: event, search_active: true});
    }
  }

  deactivateRestaurant() {
    if (this.state.active_restaurant !== false) {
      this.state.active_restaurant.image = {inactive_arrow};
      this.setState({active_restaurant: false});
      this.onRegionChangeComplete(this.state.region);
    }
  }

  activateRestaurant(event) {
    console.log(event.nativeEvent);
    for (var i = 0; i < restaurant_data.length; i++) {
      if (
        event.nativeEvent.coordinate.longitude ===
        parseFloat(restaurant_data[i].Longitude)
      ) {
        if (
          event.nativeEvent.coordinate.latitude ===
          parseFloat(restaurant_data[i].Latitude)
        ) {
          this.setState({active_restaurant: restaurant_data[i]});
        }
      }
    }
  }

  render() {
    return (
      <View style={styles.fill_container}>
        <MapView
          style={styles.fill_container}
          region={this.state.region}
          onRegionChangeComplete={this.onRegionChangeComplete}
          onPress={this.deactivateRestaurant}
          customMapStyle={my_map_style}>
          {restaurant_data.map((item, index) => {
            if (item === this.state.active_restaurant) {
              this.state.visible_count = this.state.visible_count + 1;
              return (
                <Marker
                  coordinate={{
                    latitude: parseFloat(item.Latitude),
                    longitude: parseFloat(item.Longitude),
                  }}
                  image={active_arrow}
                  onPress={this.activateRestaurant}
                  key={index}
                />
              );
            } else if (this.state.search_active === true) {
              if (
                item.tags.includes(this.state.search) ||
                item.name.includes(this.state.search)
              ) {
                this.state.visible_count = this.state.visible_count + 1;
                if (this.state.visible_count < 12) {
                  return (
                    <Marker
                      coordinate={{
                        latitude: parseFloat(item.Latitude),
                        longitude: parseFloat(item.Longitude),
                      }}
                      image={inactive_arrow}
                      onPress={this.activateRestaurant}
                      key={index}
                    />
                  );
                }
              }
            } else {
              if (CheckRestaurantVisible(this.state.region, item)) {
                this.state.visible_count = this.state.visible_count + 1;
                if (this.state.visible_count < 12) {
                  return (
                    <Marker
                      coordinate={{
                        latitude: parseFloat(item.Latitude),
                        longitude: parseFloat(item.Longitude),
                      }}
                      image={inactive_arrow}
                      onPress={this.activateRestaurant}
                      key={index}
                    />
                  );
                }
              }
            }
          })}
        </MapView>
        {this.state.active_restaurant !== false && (
          <View style={styles.restaurant_popup}>
            <ActiveRestaurantComponent
              restaurant={this.state.active_restaurant}
              style={{padding: 20, backgroundColor: 'white'}}
            />
          </View>
        )}

        <View style={styles.search_bar}>
          <SearchBar
            placeholder="Search"
            onChangeText={this.updateSearch}
            value={this.state.search}
            placeholderTextColor="black"
            searchIcon={null}
            inputContainerStyle={styles.search}
            containerStyle={{backgroundColor: 'white'}}
          />
        </View>

        <View style={styles.center_icon}>
          <TouchableOpacity
            style={styles.fill_container}
            activeOpacity={0.5}
            onPress={this.get_user_location}>
            <Image source={center_button_icon} style={styles.ImageIconStyle} />
          </TouchableOpacity>
        </View>
      </View>
    );
  }
}

const styles = StyleSheet.create({
  fill_container: {
    flex: 1,
    justifyContent: 'center',
    alignContent: 'center',
  },

  search_bar: {
    position: 'absolute',
    flex: 1,
    left: 60,
    right: 60,
    top: 30,
    borderRadius: 50,
    overflow: 'hidden',
    backgroundColor: 'white',
    justifyContent: 'space-between',
    flexDirection: 'row',
    alignItems: 'center',
  },

  search: {
    borderRadius: 50,
    backgroundColor: 'white',
    height: 25,
    width: 290,
  },

  ImageIconStyle: {
    flex: 1,
    resizeMode: 'contain',
    width: 45,
  },

  center_icon: {
    position: 'absolute',
    bottom: 15,
    right: 10,
    width: 70,
    height: 70,
    backgroundColor: 'white',
    borderRadius: 50,
    alignItems: 'center',
  },

  restaurant_popup: {
    position: 'absolute',
    left: '10%',
    right: '10%',
    top: '12%',
    borderRadius: 25,
    overflow: 'hidden',
    justifyContent: 'space-between',
    flexDirection: 'row',
    alignItems: 'center',
  },
});
