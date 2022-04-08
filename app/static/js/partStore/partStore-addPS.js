$(document).ready(function() {
    // Path to obtain the partStore list
    const getPath = '/table/part_store_list/all';
    // On submit, execute the following
    $('#btnSubmit').click(function (event) {
    // Prevents form from submitting
    event.preventDefault();
    const form = $('#formElement')[0];
    const data = new FormData(form);
    // Disable submit button until something happens
    $('#btnSubmit').prop('disabled', true);
      $.ajax({
          type: 'POST',
          enctype: 'multipart/form-data',
          url: '/parts/stores',
          data: data,
          processData: false,
          contentType: false,
          cache: false,
          timeout: 800000,
          // On success, load the span from the getPath and re-enable the submit button
          success: function () {
              $('#mySpan').load(getPath);
              $('#btnSubmit').prop('disabled', false);
              $('#instructions').html('Select a part store:').css('color', 'black');
          },
          // On failure, print errors and re-enable the submit button
          error: function (e) {
            if (e.status === 409) {
                $('#instructions').html('Duplicate entries are not allowed.').css('color', 'red');
              } else {
                console.log('ERROR : ', e);
              }
          $('#btnSubmit').prop('disabled', false);
          }
      });
      $(form).trigger('reset');
  });
});