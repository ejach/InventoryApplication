(function($) {

  // Initialize our namespace
  let namespace;

  namespace = {
    // On submit, execute the following
    deleteThis : function ($getPath) {
      let element = $('#table');
      $(document).off('click').on('click', '.deleteBtn', function(){
        let id = this.dataset.value;
        $('.deleteBtn').prop('disabled', true);
        $('.updateBtn').prop('disabled', true);
        $('#deleteBtn' + id).toggle();
        $('#updateBtn' + id).toggle();
        $('#confirmMe' + id).toggle();
        // Un-attach and re-attach the event listener
        $(element).off().on('click', '#yesBtn' + id, function () {
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
        $('.table').off().on('click', '#noBtn' + id, function () {
          $('#deleteBtn' + id).toggle();
          $('#updateBtn' + id).toggle();
          $('#confirmMe' + id).toggle();
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
      // Toggle the form/table elements
      let toggleElem = function (id) {
        if (window.location.pathname === '/parts') {
          $('#thisPartName' + id + ', #thisPartNumber' + id + ', #thisVanNumber' + id +
          ', #updateBtn' + id + ', #confirmUpdateBtn' + id + ', #deleteBtn'
          + id + ', #partName' + id + ', #partNumber' + id + ', #vanNumber' + id + ', #cancelUpdateBtn' + id).toggle();
        } else if (!window.location.pathname.split('/vans/')[1]) {
          $('#deleteBtn' + id + ', #thisVanNumber' + id + ', #vanNumber' + id + ', #updateBtn' + id + ', #confirmUpdateBtn' + id +
          ', #partNumber' + id + ', #cancelUpdateBtn' + id).toggle();
        } else {
          $('#thisPartName' + id +', #thisPartNumber' + id + ', #updateBtn' + id +
          ', #confirmUpdateBtn' + id + ', #deleteBtn' + id + ', #partName' + id + ', #partNumber' + id
          + ', #cancelUpdateBtn' + id).toggle();
        }
      }
      // Reset element passed in to its original value
      let origVal = function (elem) {
        return $(elem).attr("value");
      }
      // Get page location and return the coordinating element
      let pageElem = function () {
        let pageElem;
        if (window.location.pathname !== '/parts' && !window.location.pathname.split('/vans/')[1]) {
          pageElem = '#mySpan';
          return pageElem;
        } else if (window.location.pathname.split('/vans/')[1]) {
          pageElem = '#table';
          return pageElem;
        } else {
          pageElem = '.table';
          return pageElem;
        }
      }
      // Send POST request
      let postReq = function (url, text, reloadElem, id) {
            $.ajax({
              url: url,
              type: 'POST',
              data: text,
              success: function() {
                $(reloadElem).load($getPath);
                $('.deleteBtn').prop('disabled', false);
                $('.updateBtn').prop('disabled', false);
                toggleElem(id);
              }
            });
      }
      // On click, execute the following
      $(document.body).off('click').on('click', '.updateBtn', function(){
        // ID to be updated
        let id = this.dataset.value;
        toggleElem(id);
        let vanNum = $('#thisVanNumber'+id);
        let partName = $('#partName'+id);
        let partNumber = $('#partNumber'+id);
        let optValue = vanNum.html();
        let selectElem = $('#vanNumber'+id);
        selectElem.find('option[value="'+optValue+'"]').attr('selected',true);
        $('.deleteBtn').prop('disabled', true);
        $('.updateBtn').prop('disabled', true);
        $('#table').off('click').on('click', '#confirmUpdateBtn'+id, function(){
          let text;
          let url;
          if (!window.location.pathname.split('/')[2] && window.location.pathname !== '/parts') {
            if (selectElem.val()) {
              url = '/update/van/';
              text = 'id=' + id + '&van_number=' + selectElem.val();
              postReq(url, text, '#mySpan', id);
              $('#instructions').html('Select a van: ').css('color', 'black');
            } else {
              $('#instructions').html('Blank input will not be accepted.').css('color', 'red');
          }
          } else {
            let partNumberHtml = partNumber.val();
          let partNameHtml = partName.val();
          // If the window location is not /parts, get it from the URL, else prompt the user for the vanNum
          let vanNumHtml = (window.location.pathname !== '/parts') ? window.location.pathname.split('/')[2] : $('#vanNumber'+id+' option:selected').text();
          if (!partNameHtml || !partNumberHtml) {
            $('#instructions').html('Blank input will not be accepted.').css('color', 'red');
          } else {
            text = 'id=' + id + '&part_name=' + partNameHtml + '&part_number=' + partNumberHtml + '&van_number=' + vanNumHtml;
            $('#instructions').html('Enter the Part Name and Part Number: ').css('color', 'black');
            url = (window.location.pathname !== '/parts' && !window.location.pathname.split('/vans/')[1]) ? '/update/van/' : '/update/part/';
            postReq(url, text, '#table', id);
          }
          }
        });
        // Cancel button implementation
        $(pageElem()).off('click').on('click', '#cancelUpdateBtn'+id, function(){
          toggleElem(id);
          // Reset to original values
          if (!window.location.pathname.split('/')[2] && window.location.pathname !== '/parts') {
            selectElem.val(origVal(selectElem));
          } else {
            partName.val(origVal(partName));
            partNumber.val(origVal(partNumber));
            selectElem.val(optValue);
          }
          $('.deleteBtn').prop('disabled', false);
          $('.updateBtn').prop('disabled', false);
        });
      });
    }
  };

  // Let ns be called in the current window to access functions
  window.ns = namespace;

})(jQuery);