$(document).ready(function() {
    $("#newIng").submit(function() {
        $.ajax({
            url: $(this).attr("action"),
            data: $(this).serialize(),
            type: $(this).attr("method"),
            dataType: "html",
            success: function (a) {
                $("#newIng textarea").val("");
            }, error: function (a) {
                console.log(a);
            }
        });
        return false;
    });
}