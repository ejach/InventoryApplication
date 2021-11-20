$(document).ready(function() {
    const currentURL = (window.location.pathname);
    const getPath = '/table' + window.location.pathname;
    // Gets the number of the current van selected by the end of the pathname
    const vanNum = currentURL.split("/")[2];
    // On submit, execute the following
    $('#submit').click(function (event) {
    // Prevents form from submitting
    event.preventDefault();
    const form = $('#myForm')[0];
    const data = new FormData(form);
    // Append vanNum from URL to the formData object
    data.append('van', vanNum);
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