$(document).ready(function() {
    // Path to obtain the van list
    const getPath = '/table/vans_list/all';
    // On submit, execute the following
    $("#btnSubmit").click(function (event) {
    // Prevents form from submitting
    event.preventDefault();
    const form = $('#formElement')[0];
    const data = new FormData(form);
    // Disable submit button until something happens
    $("#btnSubmit").prop("disabled", true);
      $.ajax({
          type: 'POST',
          enctype: 'multipart/form-data',
          url: '/vans',
          data: data,
          processData: false,
          contentType: false,
          cache: false,
          timeout: 800000,
          // On success, load the span from the getPath and re-enable the submit button
          success: function () {
              $("#mySpan").load(getPath);
              $("#btnSubmit").prop("disabled", false);
          },
          // On failure, print errors and re-enable the submit button
          error: function (e) {
              console.log("ERROR : ", e);
              $("#btnSubmit").prop("disabled", false);
          }
      });
      $(form).trigger('reset');
  });
});