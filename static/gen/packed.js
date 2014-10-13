$('#btn-chk-mail').on("click", function() {
    $.ajax('/mail', {}).success(function(res) {
        console.log(res);
    });
});