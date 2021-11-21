(function($) {

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
    }
  };

  window.ns = namespace;

})(jQuery);