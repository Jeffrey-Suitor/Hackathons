export default function CheckRestaurantVisible(region, item) {
  if (region.longitude > 0) {
    var longtitude_max = region.longitude + region.longitudeDelta / 2;
    var longtitude_min = region.longitude - region.longitudeDelta / 2;
  } else {
    var longtitude_min = region.longitude + region.longitudeDelta / 2;
    var longtitude_max = region.longitude - region.longitudeDelta / 2;
  }

  if (region.latitude > 0) {
    var latitude_max = region.latitude + region.latitudeDelta / 2;
    var latitude_min = region.latitude - region.latitudeDelta / 2;
  } else {
    var latitude_min = region.latitude + region.latitudeDelta / 2;
    var latitude_max = region.latitude - region.latitudeDelta / 2;
  }

  var longitude_flag = false;
  var latitude_flag = false;
  var longitude = parseFloat(item.Longitude);
  var latitude = parseFloat(item.Latitude);

  if (region.longitude > 0) {
    if (longtitude_min <= longitude && item.Longitude <= longtitude_max) {
      //console.log("+ longitude", longtitude_min, item.Longitude, longtitude_max)
      longitude_flag = true;
    } else {
      return false;
    }
  } else {
    if (longtitude_min >= longitude && item.Longitude >= longtitude_max) {
      //console.log("- longitude", longtitude_min, item.Longitude, longtitude_max)
      longitude_flag = true;
    } else {
      return false;
    }
  }

  if (region.latitude > 0) {
    if (latitude_min <= latitude && latitude <= latitude_max) {
      //console.log("+ latitude", latitude_min, item.Latitude, latitude_max)
      latitude_flag = true;
    } else {
      return false;
    }
  } else {
    if (latitude_min >= latitude && latitude >= latitude_max) {
      //console.log("- latitude", latitude_min, item.Latitude, latitude_max)
      latitude_flag = true;
    } else {
      return false;
    }
  }

  if (latitude_flag && longitude_flag) {
    //console.log(item.name, item.Longitude, item.Latitude)
    return true;
  } else {
    return false;
  }
}
