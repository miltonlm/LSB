var map = null;

$(document).ready(function () {

    var token = $("[name=csrfmiddlewaretoken]").val();

    $("#id_ciudad, #id_tipo_inmueble, #id_zona").change(function () {
        var id = $(this).prop("id");
        var val = $(this).val();

        if (id == "id_ciudad") {

            $.ajax({
                url: "/qr/",
                method: "POST",
                data: {
                    csrfmiddlewaretoken: token,
                    funcion: "geoservice",
                    ciudad: val,
                    direccion: ""
                },
                async: false
            }).then(function (data) {
                data = JSON.parse(data);

                var array = data.results;
                var datos = array[0];
                var lat = datos.geometry.location.lat;
                var lng = datos.geometry.location.lng;

                map.setCenter(new google.maps.LatLng(lat, lng));
            });
        }
    });

});

function initMap() {
    var token = $("[name=csrfmiddlewaretoken]").val();

    map = new google.maps.Map(document.getElementById('mapa'), {
        center: {lat: 3.451647, lng: -76.531985},
        zoom: 12
    });

    $.post("/qr/", {
        csrfmiddlewaretoken: token,
        funcion: "inmuebles",
        tipo_inmueble: "",
        ubicacion: ""
    }, function (data) {
        data = JSON.parse(data);

        var markers = new Array(data.length);
        var infw = new Array(data.length);
        var i = 0;

        for (var row in data) {
            var fields = data[row].fields;

            markers[i] = new google.maps.Marker({
                position: {
                    lat: parseFloat(fields.latitud),
                    lng: parseFloat(fields.longitud)
                },
                map: map,
                label: fields.tipo_inmueble,
                fields: fields
            });

            markers[i].addListener('click', function () {
                mostrarInmueble(data);
            });

            i++;
        }
    });

    //var marker = new google.maps.Marker({position: {lat: 3.452647, lng: -76.531485}, map: map});
}

function mostrarInmueble(data) {

    for (var i in data) {
        var row = data[i].fields;


    }

}