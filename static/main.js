


var editor; // use a global for the submit and return data rendering in the examples

$(document).ready(function() {

    var btn_chk_mail = $('#btn-chk-mail');

    var btnHandle = $("#btn_handle");

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

    btn_chk_mail.on("click", function() {
        $.post('/api/mail', {}).success(function(res) {
            var tbl = table;
            if(res == 'ok') {
                tbl.api().ajax.reload(function() {
                    disableBtnHandle(true);
                });
            }

        });
    });

    $('#example tbody').on( 'click', 'tr', function () {
        if ( $(this).hasClass('selected') ) {
            $(this).removeClass('selected');
            disableBtnHandle(true);
        }
        else {
            table.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
            disableBtnHandle(false);
        }
    } );

    btnHandle.click( function () {
        var tbl = table;
        console.log(tbl.$('tr.selected'));

        
//        console.log(tbl.rows())
//        var row = tbl.row('.selected');
//        row.remove().draw(false);
//        console.log(row);
//        table.row('.selected').remove().draw( false );
    } );

    function disableBtnHandle(bool) {
        if (bool) {
            btnHandle.attr('disabled', 'disabled');
        } else {
            btnHandle.removeAttr('disabled');
        }

    }


} );


//$(document).ready(function() {
//    $('#example').dataTable( {
//        "processing": true,
//        "serverSide": true,
//        "ajax": "/api/mail"
//    } );
//} );