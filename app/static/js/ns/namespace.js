(function($) {

  // Initialize our namespace
  let namespace;

  namespace = {
    // On submit, execute the following
    deletePart : function ($getPath) {
      $(document).on('click', '.deleteBtn', function () {
        let id = this.dataset.value;
        $(".deleteBtn").prop("disabled", true);
        $('#deleteBtn' + id).hide();
        $('#updateBtn' + id).hide();
        $('#confirmMe' + id).show();
        $('.table').off('click').on('click', '#yesBtn' + id, function () {
          // Parameters to be sent in the request
          const data = 'Delete=' + id;
          $.ajax({
            type: 'POST',
            url: '/delete/part/',
            data: data,
            timeout: 800000,
            // On success, load the span from the getPath and re-enable the submit button
            success: function () {
              $('#table').load($getPath);
              $(".deleteBtn").prop("disabled", false);
            },
            // On failure, print errors and re-enable the submit button
            error: function (e) {
              console.log("ERROR : ", e);
            }
          });
        });
        $(document).on('click', '#noBtn' + id, function () {
          $('#deleteBtn' + id).show();
          $('#updateBtn' + id).show();
          $('#confirmMe' + id).hide();
          $(".deleteBtn").prop("disabled", false);
        });
      });
    },
    addPart : function ($getPath) {
      $('#submit').click(function (event) {
        // Prevents form from submitting
        event.preventDefault();
        const form = $('#myForm')[0];
        const data = new FormData(form);
        // Append vanNum from URL to the formData object if the current window is not /parts
        if (window.location.pathname !== '/parts') {
          let vanNum = window.location.pathname.split("/")[2];
          data.append('van', vanNum);
        }
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
            $('#table').load($getPath);
          },
          // On failure, print errors
          error: function (e) {
            console.log("ERROR : ", e);
          }
        });
        $(form).trigger('reset');
      });
    }
  };

  // Let ns be called in the current window to access functions
  window.ns = namespace;

})(jQuery);