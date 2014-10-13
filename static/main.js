$('#btn-chk-mail').on("click", function() {
    $.ajax('/mail', {}).success(function(res) {
        console.log(res);
    });
});


var editor; // use a global for the submit and return data rendering in the examples

$(document).ready(function() {

    $('#example').dataTable( {
        "ajax": "/api/mail",
        "serverSide": true,
        "columns": [
            { "data": "name" },
            { "data": "position" },
            { "data": "office" },
            { "data": "extn" },
            { "data": "start_date" },
            { "data": "salary" }
        ]
    } );
} );


//$(document).ready(function() {
//    $('#example').dataTable( {
//        "processing": true,
//        "serverSide": true,
//        "ajax": "/api/mail"
//    } );
//} );