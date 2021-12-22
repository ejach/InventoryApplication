$(function() {
  let registerBtn = $('#registerBtn');
  // On submit, execute the following
  $(registerBtn).click(function (event) {
    let username = $('#username').val();
    let password = $('#password').val();
    let confPass = $('#confPass').val();
    let instructions = $('#instructions');
    event.preventDefault();
    if (password === confPass && username && password && confPass) {
      // Prevents form from submitting
      const form = $('#registerForm')[0];
      const data = new FormData(form);
      // Disable submit button until something happens
      $(registerBtn).prop('disabled', true);
      $.ajax({
        type: 'POST',
        enctype: 'multipart/form-data',
        url: '/register',
        data: data,
        processData: false,
        contentType: false,
        cache: false,
        timeout: 800000,
        // On success, redirect to /login
        success: function () {
          $(registerBtn).prop('disabled', false);
          window.location.replace('/login');
        },
        // On failure, print errors and re-enable the submit button
        error: function (e) {
          console.log('ERROR : ', e);
          $(registerBtn).prop('disabled', false);
        }
      });
      $(form).trigger('reset');
      } else if (password !== confPass || !password || !confPass || !username) {
        $(instructions).html('Username, Password, and Confirm Password must not be empty and passwords must match')
            .css('color', 'red');
      } else {
        $(instructions).html('Register').css('color', 'black');
      }
  });
});