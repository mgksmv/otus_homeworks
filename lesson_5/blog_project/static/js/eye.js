$(document).on('click', '.toggle-password', function() {

    $(this).toggleClass("fa-eye fa-eye-slash");
    
    var input = $("#password_1");
    input.attr('type') === 'password' ? input.attr('type','text') : input.attr('type','password')
});

$(document).on('click', '.toggle-password-2', function() {

    $(this).toggleClass("fa-eye fa-eye-slash");

    var input = $("#password_2");
    input.attr('type') === 'password' ? input.attr('type','text') : input.attr('type','password')
});