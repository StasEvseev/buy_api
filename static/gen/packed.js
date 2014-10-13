$('#btn-chk-mail').on("click", function() {
    $.ajax('/mail', {}).success(function(res) {
        console.log(res);
    });
});

$(document).ready(function() {
    $('#example').dataTable( {
        "processing": true,
        "serverSide": true,
        "ajax": "/api/mail"
    } );
} );