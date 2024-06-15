$(document).ready(function() {
    alert("Hello World!!!!")
    $('#button1').on('click', function() {
        $(this).toggleClass('btn-danger');
    });
});