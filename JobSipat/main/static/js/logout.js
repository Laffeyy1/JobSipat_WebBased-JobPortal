$('#logoutModal').on('shown.bs.modal', function () {
    $('#logoutModal').trigger('focus')
});


$('#logoutModal').on('show.bs.modal', function (event) {
    var link = $('#myModal').data('logout.html');
    location.href = link;
});