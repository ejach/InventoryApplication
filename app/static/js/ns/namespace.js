(function($) {

  // Initialize our namespace
  let namespace;

  namespace = {
    // On submit, execute the following
    deleteThis : function ($getPath) {
      $(document).on('click', '.deleteBtn', function () {
        let id = this.dataset.value;
        let element;
        if (window.location.pathname !== '/parts' && !window.location.pathname.split('/vans/')[1]) {
          element = '#mySpan';
        } else if (window.location.pathname.split('/vans/')[1]) {
          element = '#table';
        } else {
          element = '.table';
        }
        console.log(element)
        $('.deleteBtn').prop('disabled', true);
        $('.updateBtn').prop('disabled', true);
        $('#deleteBtn' + id).hide();
        $('#updateBtn' + id).hide();
        $('#confirmMe' + id).show();
        // Un-attach and re-attach the event listener
        $(element).off('click').on('click', '#yesBtn' + id, function () {
          // Parameters to be sent in the request
          let url = (window.location.pathname !== '/parts' && !window.location.pathname.split('/vans/')[1]) ? '/delete/van/' : '/delete/part/';
          let data = 'Delete=' + id;
            $.ajax({
              type: 'POST',
              url: url,
              data: data,
              timeout: 800000,
              // On success, load the span from the getPath and re-enable the submit button
              success: function () {
                $(element).load($getPath);
                $('.deleteBtn').prop('disabled', false);
                $('.updateBtn').prop('disabled', false);
              },
              // On failure, print errors and re-enable the submit button
              error: function (e) {
                console.log('ERROR : ', e);
                $('.deleteBtn').prop('disabled', false);
                $('.updateBtn').prop('disabled', false);
              }
            });
        });
        $(document).on('click', '#noBtn' + id, function () {
          $('#deleteBtn' + id).show();
          $('#updateBtn' + id).show();
          $('#confirmMe' + id).hide();
          $('.deleteBtn').prop('disabled', false);
          $('.updateBtn').prop('disabled', false);
        });
      });
    },
    addPart : function ($getPath) {
      $('#submit').click(function (event) {
        // Prevents form from submitting
        event.preventDefault();
        $('#submit').prop('disabled', true);
        const form = $('#myForm')[0];
        const data = new FormData(form);
        // Append vanNum from URL to the formData object if the current window is not /parts
        if (window.location.pathname !== '/parts') {
          let vanNum = window.location.pathname.split('/')[2];
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
            $('#submit').prop('disabled', false);
          },
          // On failure, print errors
          error: function (e) {
            console.log('ERROR : ', e);
            $('#submit').prop('disabled', false);
          }
        });
        $(form).trigger('reset');
      });
    },
   updatePart : function($getPath) {
      // On click, execute the following
      $(document).on('click', '.updateBtn', function(){
        // ID to be updated
        let id = this.dataset.value;
        let partName = prompt('Please enter the part name:', 'PartName');
        let partNumber = prompt('Please enter the part number:', 'PartNumber');
        // If the window location is not /parts, get it from the URL, else prompt the user for the vanNum
        let vanNum = (window.location.pathname !== '/parts') ? window.location.pathname.split('/')[2] : prompt('Please enter the van number:', 'vanNumber');
        if (partName === null || partName === '' || partNumber === null || partNumber === '' || vanNum === null
            || vanNum === '') {
          alert('Blank input will not be accepted.');
        } else {
          let text = 'id=' + id + '&part_name=' + partName + '&part_number=' + partNumber + '&van_number=' + vanNum;
          // Send our POST request
          $.ajax({
            url: '/update/part/',
            type: 'POST',
            data: text,
            success: function() {
              $('#table').load($getPath);
            }
          });
        }
      });
    }
  };

  // Let ns be called in the current window to access functions
  window.ns = namespace;

})(jQuery);