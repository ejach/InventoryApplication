$(document).ready(function() {
    // Path to obtain the van table
    const getPath = '/table/main/all';
    // On submit, execute the following
    $('#submit').click(function (event) {
    // Prevents form from submitting
    event.preventDefault();
    const form = $('#myForm')[0];
    const data = new FormData(form);
      $.ajax({
          type: 'POST',
          enctype: 'multipart/form-data',
          url: '/parts',
          data: data,
          processData: false,
          contentType: false,
          cache: false,
          timeout: 800000,
          // On success, load the span from the getPath
          success: function () {
              $('#table').load(getPath);
          },
          // On failure, print errors
          error: function (e) {
              console.log("ERROR : ", e);
          }
      });
      $(form).trigger('reset');
  });
});