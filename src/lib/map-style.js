// Brand style for the neighbourhood maps (Maps JavaScript API "styles", no console set-up needed). Black, white, cream and grey only, like the site.
// Muted roads, parks a touch darker, Google's shop/restaurant pins and neighbourhood labels off (our own area labels and the nearby-places buttons replace them;
// Google's neighbourhood names are not our MLS areas). Transit stations stay. The satellite view is untouched.
export const MAP_STYLE = [
  { elementType: 'geometry', stylers: [{ color: '#f4f2ec' }] },
  { elementType: 'labels.icon', stylers: [{ visibility: 'off' }] },
  { elementType: 'labels.text.fill', stylers: [{ color: '#606060' }] },
  { elementType: 'labels.text.stroke', stylers: [{ color: '#ffffff' }, { weight: 3 }] },
  { featureType: 'administrative.land_parcel', stylers: [{ visibility: 'off' }] },
  { featureType: 'administrative.neighborhood', elementType: 'labels', stylers: [{ visibility: 'off' }] },
  { featureType: 'poi', stylers: [{ visibility: 'off' }] },
  { featureType: 'poi.park', elementType: 'geometry', stylers: [{ visibility: 'on' }, { color: '#d9dbd5' }] },
  { featureType: 'poi.park', elementType: 'labels.text', stylers: [{ visibility: 'on' }] },
  { featureType: 'poi.park', elementType: 'labels.text.fill', stylers: [{ color: '#444444' }] },
  { featureType: 'landscape.man_made', elementType: 'geometry', stylers: [{ color: '#ebe8e0' }] },
  { featureType: 'road', elementType: 'geometry', stylers: [{ color: '#ffffff' }] },
  { featureType: 'road', elementType: 'geometry.stroke', stylers: [{ color: '#dcd8ce' }] },
  { featureType: 'road.highway', elementType: 'geometry', stylers: [{ color: '#c4c4c4' }] },
  { featureType: 'road.highway', elementType: 'geometry.stroke', stylers: [{ color: '#a8a8a8' }] },
  { featureType: 'road', elementType: 'labels.text.fill', stylers: [{ color: '#707070' }] },
  { featureType: 'transit.line', elementType: 'geometry', stylers: [{ color: '#c8c8c8' }] },
  { featureType: 'transit.station', elementType: 'labels.icon', stylers: [{ visibility: 'on' }, { saturation: -100 }] },
  { featureType: 'water', elementType: 'geometry', stylers: [{ color: '#d3d6d8' }] },
  { featureType: 'water', elementType: 'labels.text.fill', stylers: [{ color: '#707070' }] },
];
