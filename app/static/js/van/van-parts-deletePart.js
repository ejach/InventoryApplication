 $(document).ready(function() {
    const getPath = '/table' + window.location.pathname;
    // On submit, execute the following
    $('.deleteMe').click(function () {
    if (window.confirm('Are you sure you want to delete?')) {
        let id = this.dataset.value;
        // Parameters to be sent in the request
        const data = 'Delete=' + id;
      $.ajax({
          type: 'POST',
          url: '/delete/part/',
          data: data,
          timeout: 800000,
          // On success, load the span from the getPath and re-enable the submit button
          success: function () {
              $('#table').load(getPath);
          },
          // On failure, print errors and re-enable the submit button
          error: function (e) {
              console.log("ERROR : ", e);
          }
      });
    }
  });
});