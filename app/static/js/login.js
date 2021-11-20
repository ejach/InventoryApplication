$(document).ready(function() {
    // On submit, execute the following
    $("#btnLogin").click(function (event) {
        // Prevents form from submitting
        event.preventDefault();
        const form = $('#loginForm')[0];
        const data = new FormData(form);
        // Disable submit button until something happens
        $("#btnLogin").prop("disabled", true);
          $.ajax({
              type: 'POST',
              enctype: 'multipart/form-data',
              url: '/login',
              data: data,
              processData: false,
              contentType: false,
              cache: false,
              timeout: 800000,
              // On success, load the span from the getPath and re-enable the submit button
              success: function () {
                  $("#btnLogin").prop("disabled", false);
                  location.reload();
              },
              // On failure, print errors and re-enable the submit button
              error: function (e) {
                  console.log("ERROR : ", e);
                  $("#btnLogin").prop("disabled", false);
              }
          });
          $(form).trigger('reset');
      });
});