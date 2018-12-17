function initMap() {

    var map = new google.maps.Map(document.getElementById('mapa'), {
        center: {lat: 3.451647, lng: -76.531985},
        zoom: 12
    });

    var marker = new google.maps.Marker({position: {lat: 3.452647, lng: -76.531485}, map: map});
}