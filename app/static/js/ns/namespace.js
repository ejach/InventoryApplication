(function($) {

  // Initialize our namespace
  let namespace;

  namespace = {
    // On submit, execute the following
    deletePart : function ($getPath) {
      $(document).on('click', '.deleteBtn', function () {
        let id = this.dataset.value;
        $(".deleteBtn").prop("disabled", true);
        $(".updateBtn").prop("disabled", true);
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
              $(".updateBtn").prop("disabled", false);
            },
            // On failure, print errors and re-enable the submit button
            error: function (e) {
              console.log("ERROR : ", e);
              $(".deleteBtn").prop("disabled", false);
              $(".updateBtn").prop("disabled", false);
            }
          });
        });
        $(document).on('click', '#noBtn' + id, function () {
          $('#deleteBtn' + id).show();
          $('#updateBtn' + id).show();
          $('#confirmMe' + id).hide();
          $(".deleteBtn").prop("disabled", false);
          $(".updateBtn").prop("disabled", false);
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
    },
   updatePart : function($getPath) {
      // On click, execute the following
      $(document).on('click', '.updateBtn', function(){
        // ID to be updated
        let id = this.dataset.value;
        let partName = prompt("Please enter the part name:", "PartName");
        let partNumber = prompt("Please enter the part number:", "PartNumber");
        let vanNum;
        // If the window location is not /parts, get it from the URL, else prompt the user for the vanNum
        if (window.location.pathname !== '/parts') {
          vanNum = window.location.pathname.split("/")[2];
        } else {
          vanNum = prompt("Please enter the van number:", "vanNumber");
        }
        if (partName === null || partName === "" || partNumber === null || partNumber === "" || vanNum === null
            || vanNum === "") {
          alert('Blank input will not be accepted.');
        } else {
          let text = 'id=' + id + '&part_name=' + partName + '&part_number=' + partNumber + '&van_number=' + vanNum;
          // Send our POST request
          $.ajax({
            url: '/update/part/',
            type: 'POST',
            data: text,
            success: function() {
              $("#table").load($getPath);
            }
          });
        }
      });
    }
  };

  // Let ns be called in the current window to access functions
  window.ns = namespace;

})(jQuery);