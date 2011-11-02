

// State 
var geocoder;           // For resolving cross streets to lat/lon coordinates
var map;                // The map
var markersArray = [];  // The set of points on the map

// Call this when you load the page for the first time and when you change the city:
// This assumes you have a div called "map_canvas" to write to.
//
// city = sfc: "San Francisco CA"
//        sby: "San Jose CA"
//        eby: "Hayward CA"
//        pen: "Mountain View CA"
//        nby: "Napa CA"
//        scz: "Santa Cruz CA"

CITY_T = {
  sfc: "San Francisco CA",
  sby: "San Jose CA",
  eby: "Hayward CA",
  pen: "Mountain View CA",
  nby: "Napa CA",
  scz: "Santa Cruz CA",
}

function mmp_initialize(city) {
  geocoder = new google.maps.Geocoder();
  geocoder.geocode({'address': city}, function(results, status) {

    if (status == google.maps.GeocoderStatus.OK) {
      var myOptions = {
        zoom: 11,
        center: results[0].geometry.location,
        mapTypeId: google.maps.MapTypeId.ROADMAP,

        mapTypeControl: false,
        panControl: true,
        zoomControl: true,
        scaleControl: true,
        streetViewControl: false  
      };

    } else {
      alert("Geocode was not successful for the following reason: " + status);
    }

    map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);

  });  
}

// This should be called by dropPins:
// address = xloc0 " at " xloc1
// title   = posting title
// posting = full posting text

function mmp_dropPin(address, title, posting) {
  geocoder.geocode({'address': address}, function(results, status) {
    if (status == google.maps.GeocoderStatus.OK) {

      var marker = new google.maps.Marker({
        map: map,
        animation: google.maps.Animation.DROP,
        draggable: false,
        position: results[0].geometry.location,
        title: title
      });

      var infowindow = new google.maps.InfoWindow({content: posting});

      google.maps.event.addListener(marker, 'click', function() {
        infowindow.open(map,marker);
      });

      markersArray.push(marker);

    } else {
      alert("Geocode was not successful for the following reason: " + status);
    }
  });
}

// This should iterate over search results, calling dropPin with the appropriate values
// locations = Temporary data

var locations = ["2801 Greenwich at Baker", 
"1845 Franklin Street", 
"ST.GERMAIN at GLENBROOK", 
"Manzanita at Euclid"];

function mmp_dropPins() {
  for ( var i = 0; i < locations.length; i++ ) {
    (function(idx) {
      setTimeout(function() {
        mmp_dropPin(locations[idx], locations[idx], locations[idx]);
        }, idx * 200);
        })(i);  
      }  
    }

// Call this whenever you need to repopulate the map with new data

function mmp_clearPins() {
  if (markersArray) {
    for (i in markersArray) {
      markersArray[i].setMap(null);
    }
  }
}
