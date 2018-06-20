$(document).ready(function() {
    var id = 0;
    $.ajax({
        url: '/Ingresos',
        dataType: 'json',
        success: function (a) {
            $(".tGastos").html("");
            if (a.tipo == 1) {
                $.each(a["datos"], function (i, v) {
                    $(".tGastos").append('<div class="nGst" data-id="'+v['id']+'" data-name="'+v['nombre']+'">'
                                                + '<p class="name">'+v['nombre']+'</p>'
                                                + '<p class="cant">'+v['cant']'</p>'
                                                + '</div>');
                });
            }
        }, error: function (a) {
            console.log(a);
        }
    });
}