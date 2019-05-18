$(document).ready(function () {
    // Activate tooltip
    $('[data-toggle="tooltip"]').tooltip();

    $('.form-bootstrap input, .form-bootstrap select, .form-bootstrap textarea').each(function () {
        if ($(this).prop("type") == "checkbox") {
            return;
        }

        $(this).addClass("form-control");
    });

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

    //trp.after("<tr><td></td><td><input id='id_nombre_propietario' type='text' class='form-control' disabled></td></tr>");
    tr.after("<tr id='tr_imagen'><td></td><td id='td_imagen'></td></tr>");
    tr.after("<tr><td></td><td><input id='id_direccion_texto' type='text' class='form-control' disabled></td></tr>");

    /*$("#id_cliente_propietario").change(function () {
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
    });*/

    var container = $("#id_inmueble");

    if (container != null) {

        /*$("#id_cliente_arrendatario").parent().parent().after("<tr><td></td><td><input id='id_nombre_cliente' type='text' class='form-control' disabled></td></tr>");

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
                        $("#id_nombre_cliente").val("");
                        swal("Error", "El cliente arrendatario indicado no existe.", "error");
                        return;
                    }

                    var cp = data[0];

                    $("#id_nombre_cliente").val(cp.fields.nombre);
                });

            }
        });*/

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

    $("#edit_modal input, #edit_modal select, #edit_modal textarea").each(function (index) {
        var id = $(this).prop("id");

        $(this).prop("id", id.replace("id_", "edid_"));
    });

    var pais = $("#edit_modal").find("[name=pais]");

    if (pais.length > 0) {
        $.ajax({
            url: "/qr/",
            method: "get",
            data: {
                funcion: "paises"
            },
            success: function (rp) {
                pais.html("<option value=''>SELECCIONAR</option>");

                for (var i in rp) {
                    var row = rp[i];

                    pais.append("<option value='" + row.pk + "'>" + row.fields["nombre"] + "</option>");
                }

                pais.val('');
            }
        });

        var departamentos = $("#edit_modal").find("[name=departamento]");
        var ciudad = $("#edit_modal").find("[name=ciudad]");

        pais.change(function () {
            if (pais.val() == '') {
                return;
            }

            $.ajax({
                url: "/qr/",
                method: "get",
                data: {
                    funcion: "departamentos",
                    pais: pais.val()
                },
                success: function (rp) {
                    departamentos.html("<option value=''>SELECCIONAR</option>");

                    for (var i in rp) {
                        var row = rp[i];

                        departamentos.append("<option value='" + row.pk + "'>" + row.fields["nombre"] + "</option>");
                    }

                    departamentos.val('');
                    ciudad.val('');
                }
            });
        });

        departamentos.change(function () {
            if (departamentos.val() == '') {
                return;
            }

            $.ajax({
                url: "/qr/",
                method: "get",
                data: {
                    funcion: "ciudades",
                    departamento: departamentos.val()
                },
                success: function (rp) {
                    ciudad.html("<option value=''>SELECCIONAR</option>");

                    for (var i in rp) {
                        var row = rp[i];

                        ciudad.append("<option value='" + row.pk + "'>" + row.fields["nombre"] + "</option>");
                    }

                    ciudad.val('');
                }
            });
        });
    }
});

function geoimage(location) {
    var token = $("[name=csrfmiddlewaretoken]").val();

    $("#id_location").val(location);
    $("#id_form_imagen").submit();
}

function nombrePropietario() {

}

function editar(id) {
    var tabla = $("#tabla").val();

    $("#edit_modal .edid_id").val(id);

    $.ajax({
        url: "/crud/" + tabla + "/" + id,
        method: "GET",
        data: {
            id: id
        },
        success: function (rp) {
            var obj = rp[0];

            for (var i in obj.fields) {
                var f = $("#edid_" + i);
                var input = $("#edit_modal [name=" + i + "]");

                if (input.prop("type") == "checkbox") {
                    var vals = obj.fields[i];
                    var json = JSON.parse(vals.replace(/'/g, "\""));

                    for (var i in json) {
                        var cv = json[i];

                        input.each(function () {
                            if ($(this).val() == cv) {
                                $(this).prop("checked", true);
                            }
                        });
                    }
                } else {
                    f.val(obj.fields[i]).change();
                }
            }
        }
    });
}

function eliminar(id) {
    var tabla = $("#tabla").val();
    var token = $("[name=csrfmiddlewaretoken]").val();

    $.ajax({
        url: "/crud/" + tabla + "/" + id,
        method: "DELETE",
        success: function (rp) {
            if (rp.ok) {
                Swal.fire("Ok", "Registro eliminado correctamente", "success").then(function () {
                    document.location.reload();
                });
            }
        }
    });
}

function submitForm(event, form) {
    var tabla = $("#tabla").val();

    event.preventDefault();

    form = $(form);

    var modify = false;
    var url = "";

    if (form.find(".edid_id").length > 0) {
        url = "/" + form.find(".edid_id").val();
        modify = true;
    }

    $.ajax({
        url: "/crud/" + tabla + url,
        method: 'POST',
        data: form.serialize(),
        success: function (rp) {
            if (rp.ok) {
                if (modify) {
                    Swal.fire("Ok", "Registro actualizado correctamente", "success").then(function () {
                        document.location.reload();
                    });
                } else {
                    Swal.fire("Ok", "Registro agregado correctamente", "success").then(function () {
                        document.location.reload();
                    });
                }
            } else {
                if (modify) {
                    Swal.fire("Error", "Error al actualizar el registro", "error");
                } else {
                    Swal.fire("Error", "Error al crear el registro", "error");
                }

            }
        }
    });
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