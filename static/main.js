$('#btn-chk-mail').on("click", function() {
    $.ajax('/mail', {}).success(function(res) {
        console.log(res);
    });
});


var editor; // use a global for the submit and return data rendering in the examples

$(document).ready(function() {

    var table = $('#example').dataTable( {
        "ajax": "/api/mail",
        "serverSide": true,
        "columns": [
            { "data": "date" },
            { "data": "title" },
            { "data": "from" },
        ],
        "createdRow": function ( row, data, index ) {
            if (!data['is_handling']) {
                $(row).addClass("not_handle");
            }
        },
        "bSort": false
    });

    var btnHandle = $("#btn_handle");

    $('#example tbody').on( 'click', 'tr', function () {
        if ( $(this).hasClass('selected') ) {
            $(this).removeClass('selected');
            btnHandle.attr('disabled', 'disabled');
        }
        else {
            table.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
            btnHandle.removeAttr('disabled');
        }
    } );

    btnHandle.click( function () {
        table.row('.selected').remove().draw( false );
    } );


} );


//$(document).ready(function() {
//    $('#example').dataTable( {
//        "processing": true,
//        "serverSide": true,
//        "ajax": "/api/mail"
//    } );
//} );