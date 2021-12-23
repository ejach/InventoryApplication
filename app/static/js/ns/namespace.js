(function($) {

  // Initialize our namespace
  let namespace;

  // Toggle elements
  let toggleMe = function () {
    for (let i=0; i < arguments.length; i++) {
      let elem = arguments[i];
      $(elem).toggle();
    }
  }

  // Toggle the props that are passed through
  let toggleProps = function () {
    for (let i=0; i < arguments.length; i++) {
      let elem = arguments[i];
      if ($(elem).prop('disabled') === true) {
        $(elem).prop('disabled', false);
      } else {
        $(elem).prop('disabled', true);
      }
    }
  }

  // Set CSRF token for the namespace per the WTForms documentation
  let csrfToken = $('meta[name=csrf-token]').attr('content');
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrfToken)
      }
    }
  });

  namespace = {
    // On submit, execute the following
    deleteThis : function ($getPath) {
      let element = $('#table');
      $(document).off().on('click', '.deleteBtn', function(){
        let id = this.dataset.value;
        toggleProps('.deleteBtn', '.updateBtn');
        toggleMe('#deleteBtn' + id, '#updateBtn' + id, '#confirmMe' + id);
        // Un-attach and re-attach the event listener
        $(element).off().on('click', '#yesBtn' + id, function () {
          // Parameters to be sent in the request
          let url = (window.location.pathname !== '/parts' && !window.location.pathname.split('/vans/')[1]) ? '/delete/van/' : '/delete/part/';
          // Append csrf token to data string
          let data = 'Delete=' + id + '&csrf_token=' + csrfToken;
          $.ajax({
            type: 'POST',
            url: url,
            data: data,
            timeout: 800000,
            // On success, load the span from the getPath and re-enable the submit button
            success: function () {
              $(element).load($getPath);
              toggleProps('.deleteBtn', '.updateBtn');
            },
            // On failure, print errors and re-enable the submit button
            error: function (e) {
              console.log('ERROR : ', e);
              toggleProps('.deleteBtn', '.updateBtn');
            }
          });
        });
        $('.table').off().on('click', '#noBtn' + id, function () {
          toggleMe('#deleteBtn' + id, '#updateBtn' + id, '#confirmMe' + id);
          toggleProps('.deleteBtn', '.updateBtn');
        });
      });
    },
    addPart : function ($getPath) {
      $('#submit').click(function (event) {
        // Prevents form from submitting
        event.preventDefault();
        toggleProps('#submit');
        const form = $('#myForm')[0];
        const data = new FormData(form);
        // Append csrf token to data object
        data.append('csrf_token', csrfToken);
        let amount = $('#partAmount');
        let partName = $('#partName');
        let partNumber = $('#partNumber');
        let instructions = $('#instructions');
        let vanNum = window.location.pathname.split('/')[2] ? window.location.pathname.split('/')[2] : $('#van').val();
        // Append vanNum from URL to the formData object if the current window is not /parts
        if (window.location.pathname !== '/parts') {
          let vanNum = window.location.pathname.split('/')[2];
          data.append('van', vanNum);
        }
        if (!Number.isFinite(amount) && amount.val() && partName.val() && partNumber.val() && vanNum) {
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
              toggleProps('#submit');
              $(instructions).html('Enter the Part Name, Part Number, and Part Amount: ')
              .css('color', 'black');
            },
            // On failure, print errors
            error: function (e) {
              console.log('ERROR : ', e);
              toggleProps('#submit');
            }
          });
          $(form).trigger('reset');
          // If amount is blank, or the amount is NaN notify the user
        } else if (Number.isNaN(amount) || !amount.val() || !partName.val() || !partNumber.val() || !vanNum) {
          $(instructions).html('Invalid or blank input').css('color', 'red');
          toggleProps('#submit');
        }
      });
    },
    updatePart : function($getPath) {
      // Toggle the form/table elements
      let toggleElem = function (id) {
        if (window.location.pathname === '/parts') {
          $('#thisPartName' + id + ', #thisPartNumber' + id + ', #thisVanNumber' + id + ', #thisAmount' + id +
          ', #newPartAmount' + id + ', #updateBtn' + id + ', #confirmUpdateBtn' + id + ', #deleteBtn'
          + id + ', #partName' + id + ', #partNumber' + id + ', #vanNumber' + id + ', #cancelUpdateBtn' + id).toggle();
        } else if (!window.location.pathname.split('/vans/')[1]) {
          $('#deleteBtn' + id + ', #thisVanNumber' + id + ', #vanNumber' + id + ', #updateBtn' + id +
          ', #confirmUpdateBtn' + id +  ', #partNumber' + id + ', #cancelUpdateBtn' + id).toggle();
        } else {
          $('#thisPartName' + id +', #thisPartNumber' + id + ', #updateBtn' + id + ', #thisAmount' + id +
          ', #newPartAmount' + id + ', #confirmUpdateBtn' + id + ', #deleteBtn' + id + ', #partName' + id +
          ', #partNumber' + id  + ', #cancelUpdateBtn' + id).toggle();
        }
      }
      // Reset element passed in to its original value
      let origVal = function (elem) {
        return $(elem).attr("value");
      }

      // Send POST request
      let postReq = function (url, text, reloadElem, id) {
        $.ajax({
          url: url,
          type: 'POST',
          // Append the csrf token to the data string
          data: text + '&csrf_token=' + csrfToken,
          success: function() {
            $(reloadElem).load($getPath);
            toggleProps('.deleteBtn', '.updateBtn');
            toggleElem(id);
          }
        });
      }
      // On click, execute the following
      $(document.body).off().on('click', '.updateBtn', function(){
        // ID to be updated
        let id = this.dataset.value;
        toggleElem(id);
        let vanNum = $('#thisVanNumber'+id);
        let partName = $('#partName'+id);
        let partNumber = $('#partNumber'+id);
        let optValue = vanNum.html();
        let selectElem = $('#vanNumber'+id);
        let partAmount = $('#newPartAmount'+id);
        // Make sure the select element selects the original value
        selectElem.find('option[value="'+optValue+'"]').attr('selected',true);
        toggleProps('.deleteBtn', '.updateBtn');
        $('#table').off('click').on('click', '#confirmUpdateBtn'+id, function() {
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
            let partAmountHtml = partAmount.val();
            // If the window location is not /parts, get it from the URL, else prompt the user for the vanNum
            let vanNumHtml = (window.location.pathname !== '/parts') ? window.location.pathname.split('/')[2] : $('#vanNumber'+id+' option:selected').text();
            if (!partNameHtml || !partNumberHtml || !partAmountHtml) {
              $('#instructions').html('Blank input will not be accepted.').css('color', 'red');
            } else {
              text = 'id=' + id + '&part_name=' + partNameHtml + '&part_amount=' + partAmountHtml + '&part_number=' + partNumberHtml + '&van_number=' + vanNumHtml;
              $('#instructions').html('Enter the Part Name and Part Number: ').css('color', 'black');
              url = (window.location.pathname !== '/parts' && !window.location.pathname.split('/vans/')[1]) ? '/update/van/' : '/update/part/';
              postReq(url, text, '#table', id);
            }
          }
        });
        // Cancel button implementation
        $('.table').off().on('click', '#cancelUpdateBtn'+id, function(){
          toggleElem(id);
          // Reset to original values
          if (!window.location.pathname.split('/')[2] && window.location.pathname !== '/parts') {
            selectElem.val(origVal(selectElem));
          } else {
            partName.val(origVal(partName));
            partNumber.val(origVal(partNumber));
            partAmount.val(origVal(partAmount));
            selectElem.val(optValue);
          }
          toggleProps('.deleteBtn', '.updateBtn');
        });
      });
    },
    loginUser : function () {
      let username = $('#username');
    let password = $('#password');
    let instructions = $('#instructions');
    let btnLogin = $('#btnLogin');
    // On submit, execute the following
    $(btnLogin).click(function (event) {
        if (!username.val() || !password.val()) {
            $(instructions).html('Blank input will not be accepted.').css('color', 'red');
        } else {
            // Prevents form from submitting
            event.preventDefault();
            const form = $('#loginForm')[0];
            const data = new FormData(form);
            // Append csrf token to data object
            data.append('csrf_token', csrfToken);
            // Disable submit button until something happens
            $(btnLogin).prop('disabled', true);
            $.ajax({
                type: 'POST',
                enctype: 'multipart/form-data',
                url: '/login',
                data: data,
                processData: false,
                contentType: false,
                cache: false,
                timeout: 800000,
                // On success, load the span from the getPath and re-enable the submit button
                success: function () {
                    $(btnLogin).prop('disabled', false);
                    $(instructions).html('Login').css('color', 'black');
                    location.reload();
                },
                // On failure, print errors and re-enable the submit button
                error: function (e) {
                    if (e.status === 401) {
                        $(instructions).html('Incorrect login credentials').css('color', 'red');
                    } else {
                        console.log('ERROR : ', e);
                    }
                    $(btnLogin).prop('disabled', false);
                }
            });
            $(form).trigger('reset');
        }
      });
    },
        registerUser : function () {
          let registerBtn = $('#registerBtn');
          // On submit, execute the following
          $(registerBtn).click(function (event) {
            let username = $('#username').val();
            let password = $('#password').val();
            let confPass = $('#confPass').val();
            let instructions = $('#instructions');
            event.preventDefault();
            if (password === confPass && username && password && confPass) {
              // Prevents form from submitting
              const form = $('#registerForm')[0];
              const data = new FormData(form);
              // Append csrf token to data object
              data.append('csrf_token', csrfToken);
              // Disable submit button until something happens
              $(registerBtn).prop('disabled', true);
              $.ajax({
                type: 'POST',
                enctype: 'multipart/form-data',
                url: '/register',
                data: data,
                processData: false,
                contentType: false,
                cache: false,
                timeout: 800000,
                // On success, redirect to /login
                success: function () {
                  $(registerBtn).prop('disabled', false);
                  window.location.replace('/login');
                },
                // On failure, print errors and re-enable the submit button
                error: function (e) {
                  if (e.status === 409) {
                    $(instructions).html('Username already exists, please try again').css('color', 'red');
                    } else {
                    console.log('ERROR : ', e);
                  }
                  $(registerBtn).prop('disabled', false);
                }
              });
              $(form).trigger('reset');
              } else if (password !== confPass || !password || !confPass || !username) {
                $(instructions).html('Username, Password, and Confirm Password must not be empty and passwords must match')
                    .css('color', 'red');
              } else {
                $(instructions).html('Register').css('color', 'black');
              }
          });
        }
  };

  // Let ns be called in the current window to access functions
  window.ns = namespace;

})(jQuery);