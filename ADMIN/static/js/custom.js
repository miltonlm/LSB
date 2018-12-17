$(document).ready(function () {

    // Activate tooltip
    $('[data-toggle="tooltip"]').tooltip();

    // Select/Deselect checkboxes
    var checkbox = $('table tbody input[type="checkbox"]');

    $("#selectAll").click(function () {
        if (this.checked) {
            checkbox.each(function () {
                this.checked = true;
            });
        } else {
            checkbox.each(function () {
                this.checked = false;
            });
        }
    });

    checkbox.click(function () {
        if (!this.checked) {
            $("#selectAll").prop("checked", false);
        }
    });

    var token = $("[name=csrfmiddlewaretoken]").val();
    var trp = $("#id_cliente_propietario").parent().parent();
    var tr = $("#id_direccion").parent().parent();

    trp.after("<tr><td></td><td><input id='id_nombre_propietario' type='text' class='form-control' disabled></td></tr>");
    tr.after("<tr id='tr_imagen'><td></td><td id='td_imagen'></td></tr>");
    tr.after("<tr><td></td><td><input id='id_direccion_texto' type='text' class='form-control' disabled></td></tr>");

    $("#id_cliente_propietario").change(function () {
        var token = $("[name=csrfmiddlewaretoken]").val();
        var id = $(this).val();

        if (id && id.length > 5) {

            $.ajax({
                url: "/qr/",
                method: "POST",
                data: {
                    csrfmiddlewaretoken: token,
                    funcion: "cliente_propietario",
                    id: id
                },
                async: false
            }).then(function (data) {
                data = JSON.parse(data);

                if (data.length == 0) {
                    $("#id_nombre_propietario").val("");
                    swal("Error", "El cliente propietario indicado no existe.", "error");
                    return;
                }

                var cp = data[0];

                $("#id_nombre_propietario").val(cp.fields.nombre);

                cargarInmuebles(id);
            });

        }
    });

    var container = $("#id_inmueble");

    if (container != null) {

        $("#id_cliente_arrendatario").parent().parent().after("<tr><td></td><td><input id='id_nombre_cliente' type='text' class='form-control' disabled></td></tr>");

        $("#id_cliente_arrendatario").change(function () {
            var token = $("[name=csrfmiddlewaretoken]").val();
            var id = $(this).val();

            if (id && id.length > 5) {

                $.ajax({
                    url: "/qr/",
                    method: "POST",
                    data: {
                        csrfmiddlewaretoken: token,
                        funcion: "cliente_arrendatario",
                        id: id
                    },
                    async: false
                }).then(function (data) {
                    data = JSON.parse(data);

                    if (data.length == 0) {
                        $("#id_nombre_propietario").val("");
                        swal("Error", "El cliente arrendatario indicado no existe.", "error");
                        return;
                    }

                    var cp = data[0];

                    $("#id_nombre_cliente").val(cp.fields.nombre);
                });

            }
        });

    }

    $("#id_direccion").change(function () {

        var val = $(this).val();
        var ciudad = $("#id_ciudad option:selected").text();

        if (val && val.length > 10) {

            $.ajax("/qr/", {
                method: "POST",
                data: {
                    csrfmiddlewaretoken: token,
                    funcion: "geoservice",
                    ciudad: ciudad,
                    direccion: val
                }
            }).then(function (data) {
                data = JSON.parse(data);

                var array = data.results;

                if (array.length == 0) {
                    swal("Error", "La dirección es incorrecta", "error");
                    return;
                } else if (array.length > 1) {
                    swal("Error", "La dirección retorna más de un resultado", "error");
                    return;
                }

                var datos = array[0];
                var fa = datos.formatted_address;
                var lat = datos.geometry.location.lat;
                var lng = datos.geometry.location.lng;
                var loc = lat + "," + lng;
                var imagen = $("<img />");

                $("#id_latitud").val(lat);
                $("#id_longitud").val(lng);
                $("#id_direccion_texto").val(fa);

                imagen.prop("src", "/qr/?funcion=geoimage&location=" + encodeURI(loc));

                $("#td_imagen").html(imagen);
            });

        }

    });

    /*$('#tabla_programa').footable({
        "paging": {
            "enabled": true
        },
        "filtering": {
            "enabled": true
        },
        "sorting": {
            "enabled": true
        }
    });*/

    $("#tabla_programa").DataTable({
        responsive: true
    });
});

function geoimage(location) {
    var token = $("[name=csrfmiddlewaretoken]").val();

    $("#id_location").val(location);
    $("#id_form_imagen").submit();

}

function nombrePropietario() {

}

function editar(id) {
    alert("HOLA " + id);
}

function cargarInmuebles(cp) {
    var token = $("[name=csrfmiddlewaretoken]").val();
    var container = $("#id_inmueble");

    if (container != null) {

        $.post("/qr/", {
            csrfmiddlewaretoken: token,
            funcion: "inmuebles_propietario",
            id: cp
        }, function (rp) {
            rp = JSON.parse(rp);

            container.html("<option value=''>SELECCIONAR</option>");

            for (var i in rp) {
                var row = rp[i];
                var fields = row.fields;

                container.append("<option value='" + row.pk + "'>" + fields.tipo_inmueble + ", " + fields.barrio + ", " + fields.direccion + "</option>");
            }
        });

    }

}