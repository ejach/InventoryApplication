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

  // Reset element passed in to its original value
      let origVal = function (elem) {
        return $(elem).attr('value');
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

  // Toggle input
  let toggleInput = function () {
    for (let i=0; i < arguments.length; i++) {
      let elem = arguments[i];
      if ($(elem).attr('disabled') === 'disabled') {
        $(elem).attr('disabled', false);
      } else {
        $(elem).attr('disabled', true);
      }
    }
  }

  // POST request function
  let postRequest = function (url, data, toggles, enctype, getPath, extras, type) {
    $('html').css('cursor', 'progress');
    if (type !== 'insert' && type !== 'thresh') {
      $.ajax({
        type: 'POST',
        enctype: enctype,
        url: url,
        data: data,
        cache: false,
        timeout: 800000,
        // On success, load the span from the getPath
        success: function () {
          $('#table').load(getPath);
          toggleProps(toggles);
          $('html').css('cursor', 'default');
          return extras;
        },
        // On failure, print errors
        error: function (e) {
          if (e.status === 409) {
            $('#instructions').html('Duplicate entries are not allowed.').css('color', 'red');
          } else {
            console.log('ERROR : ', e);
          }
          toggleProps(toggles);
          $('html').css('cursor', 'default');
        }
      });
    } else if (type === 'thresh') {
      $.ajax({
        type: 'POST',
        enctype: enctype,
        url: url,
        data: data,
        cache: false,
        timeout: 800000,
        // On success, load the span from the getPath
        success: function () {
          $('#info').load(getPath);
          toggleProps(toggles);
          $('html').css('cursor', 'default');
        },
        // On failure, print errors
        error: function (e) {
          console.log('ERROR : ', e);
          toggleProps(toggles);
          $('html').css('cursor', 'default');
        }
      });
    } else if (type === 'insert') {
      $.ajax({
        type: 'POST',
        enctype: enctype,
        url: url,
        data: data,
        processData: false,
        contentType: false,
        cache: false,
        timeout: 800000,
        // On success, load the span from the getPath
        success: function () {
          $('#table').load(getPath);
          toggleProps(toggles);
          $('html').css('cursor', 'default');
          return extras;
        },
        // On failure, print errors
        error: function (e) {
          console.log('ERROR : ', e);
          toggleProps(toggles);
          $('html').css('cursor', 'default');
        }
      });
    }
  }

  // Set CSRF token in the header for the namespace per the WTForms documentation
  let csrfToken = $('meta[name=csrf-token]').attr('content');
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader('X-CSRFToken', csrfToken)
      }
    }
  });

  namespace = {
    // On submit, execute the following
    deleteThis : function ($getPath) {
      let element = $('#table');
      $(document).off('click').on('click', '.deleteBtn', function(){
        let id = this.dataset.value;
        toggleProps('.deleteBtn', '.updateBtn');
        toggleMe('#deleteBtn' + id, '#updateBtn' + id, '#confirmMe' + id);
        // Un-attach and re-attach the event listener
        $(element).off().on('click', '#yesBtn' + id, function () {
          toggleProps('#yesBtn' + id);
          // Parameters to be sent in the request
          let url = (window.location.pathname.split('/')[2] !== 'type' && window.location.pathname !== '/parts'
              && !window.location.pathname.split('/vans/')[1]) ? '/delete/van/' : '/delete/part/';
          // Append csrf token to data string
          let data = 'Delete=' + id;
          let toggles = ['.deleteBtn', '.updateBtn'].toString();
          postRequest(url, data, toggles, 'multipart/form-data', $getPath);
        });
        $('#noBtn' + id).off().click(function () {
          toggleMe('#deleteBtn' + id, '#updateBtn' + id, '#confirmMe' + id);
          toggleProps('.deleteBtn', '.updateBtn');
        });
      });
    },
    updateThresh : function ($getpath) {
     $(document).off('click').on('click', '.updateThresh', function () {
        let updateBtn = $('#updateThresh');
        let submitBtn = $('#submitBtn');
        let cancelBtn = $('#cancelBtn')
        let myThresh = $('#myThresh');
        let newThresh = $('#newThresh');
        let instructions = $('#instructions');
        toggleMe(newThresh, submitBtn, updateBtn, myThresh, cancelBtn);
        $(submitBtn).off('click').click(function () {
          if (Number.isFinite(newThresh) || !newThresh.val() || !(newThresh.val() > 0)) {
            $(instructions).html('Invalid or blank input will not be accepted').css('color', 'red');
          } else {
            let toggles = ['#newThresh', '#submitBtn', '#cancelBtn'].toString();
            let data = 'newThresh=' + newThresh.val() + '&id=' + $('#id').val();
            postRequest('/update/threshold', data, toggles, null, $getpath, null, 'thresh');
            toggleMe(newThresh, submitBtn, updateBtn, myThresh, cancelBtn);
            $(instructions).html('Part Information').css('color', 'black');
          }
        });
      });
      $('.main').off('click').on('click', '.cancelBtn',  function () {
        $('#myThresh').val(origVal('#myThresh'));
        toggleMe('#myThresh', '#submitBtn', '#updateThresh', '#newThresh', '#cancelBtn');
      });
    },
    addPart : function ($getPath) {
      $('#submit').click(function (event) {
        // Prevents form from submitting
        event.preventDefault();
        toggleProps('#submit');
        const form = $('#myForm')[0];
        const data = new FormData(form);
        let amount = $('#partAmount');
        let partName = $('#partName');
        let partNumber = $('#partNumber');
        let unit = $('#unit').val();
        let instructions = $('#instructions');
        let vanNum = window.location.pathname.split('/')[2] ? window.location.pathname.split('/')[2] : $('#van').val();
        // Append vanNum from URL to the formData object if the current window is not /parts
        if (window.location.pathname !== '/parts') {
          let vanNum = window.location.pathname.split('/')[2];
          data.append('van', vanNum);
        }
        if (!Number.isFinite(amount) && amount.val() && partName.val() && partNumber.val() && vanNum && unit &&
        parseInt(amount.val()) !== amount.val() && parseInt(amount.val()) > 0) {
          postRequest('/parts', data, ('#submit'), 'multipart/form-data', $getPath,window.location.pathname.split('/')[2]
          ? $(instructions).html('Enter the Part Name, Part Number, and Part Amount: ').css('color', 'black')
          : $(instructions).html('Enter the Part Name, Part Number, Part Amount, and Van Number: ').css('color', 'black'), 'insert');
          $(form).trigger('reset');
          // If amount is blank, or the amount is NaN notify the user
        } else {
          $(instructions).html('Invalid or blank input will not be accepted').css('color', 'red');
          setTimeout(function () {
            toggleProps('#submit');
          }, 3000);
        }
      });
    },
    updatePart : function($getPath) {
      // Toggle the form/table elements
      let toggleElem = function (id) {
        if (window.location.pathname === '/parts' || window.location.pathname.split('/type')[1]) {
          $('#thisPartName' + id + ', #thisPartNumber' + id + ', #thisVanNumber' + id + ', #thisAmount' + id +
              ', #newPartAmount' + id + ', #updateBtn' + id + ', #confirmUpdateBtn' + id + ', #deleteBtn'
              + id + ', #partName' + id + ', #partNumber' + id + ', #vanNumber' + id + ', #cancelUpdateBtn' + id +
              ' , #thisPartUnit' + id + ' , #newUnit' + id).toggle();
        } else if (!window.location.pathname.split('/vans/')[1]) {
          $('#deleteBtn' + id + ', #thisVanNumber' + id + ', #vanNumber' + id + ', #updateBtn' + id +
          ', #confirmUpdateBtn' + id +  ', #partNumber' + id + ', #cancelUpdateBtn' + id).toggle();
        } else {
          $('#thisPartName' + id +', #thisPartNumber' + id + ', #updateBtn' + id + ', #thisAmount' + id +
          ', #newPartAmount' + id + ', #confirmUpdateBtn' + id + ', #deleteBtn' + id + ', #partName' + id +
          ', #partNumber' + id  + ', #cancelUpdateBtn' + id + ' , #thisPartUnit' + id + ' , #newUnit' + id).toggle();
        }
      }

      $(document.body).off().on('click', '.updateBtn', function(){
        // ID to be updated
        let id = this.dataset.value;
        toggleElem(id);
        let vanNum = $('#thisVanNumber'+id);
        let partName = $('#partName'+id);
        let partNumber = $('#partNumber'+id);
        let vanNumOptVal = vanNum.html();
        let selectVanElem = $('#vanNumber'+id);
        let partAmount = $('#newPartAmount'+id);
        let selectUnit = $('#thisPartUnit' + id);
        let selectUnitElem = $('#newUnit' + id);
        let partUnitOptVal = selectUnit.html();
        let instructions = $('#instructions');
        // Make sure the select element selects the original value
        selectVanElem.find('option[value="'+vanNumOptVal+'"]').attr('selected',true);
        selectUnitElem.find('option[value="'+partUnitOptVal+'"]').attr('selected',true);
        toggleProps('.deleteBtn', '.updateBtn');
        $('#table').off('click').on('click', '#confirmUpdateBtn'+id, function(event) {
          let text;
          let url;
          toggleElem(id);
          if (!window.location.pathname.split('/')[2] && window.location.pathname !== '/parts') {
            if (selectVanElem.val()) {
              url = '/update/van/';
              text = 'id=' + id + '&vanNumber=' + selectVanElem.val();
              let toggles = ['.deleteBtn', '.updateBtn'].toString();
              // Send our POST request
              postRequest(url, text, toggles, null, $getPath);
              $(instructions).html('Select a van: ').css('color', 'black');
            } else {
              $(instructions).html('Blank input will not be accepted.').css('color', 'red');
            }
          } else {
            let partNumberHtml = partNumber.val();
            let partNameHtml = partName.val();
            let partAmountHtml = partAmount.val();
            let partUnitHtml = $('#newUnit'+id+' option:selected').text();
            // If the window location is not /parts, get it from the URL, else prompt the user for the vanNum
            let vanNumHtml = function() {
              if (window.location.pathname !== '/parts' && window.location.pathname.split('/')[2] && !window.location.pathname.split('/')[3]) {
                return window.location.pathname.split('/')[2];
              } else {
                 return $('#vanNumber'+id+' option:selected').text();
              }
            };
            if (!partNameHtml || !partNumberHtml || !partAmountHtml || parseInt(partAmountHtml) < 0) {
              $(instructions).html('Blank or invalid input will not be accepted.').css('color', 'red');
              toggleProps('.deleteBtn', '.updateBtn');
              origVal('#newPartAmount' + id);
            } else {
              let newInstructions = function () {
                if (window.location.pathname.split('/')[2] !== 'type' || window.location.pathname.split('/')[2] !== 'parts'
                    && !window.location.pathname.split('/')[3]) {
                  return $(instructions).html('Enter the Part Name, Part Number, and Part Amount: ').css('color', 'black');
                } else if (window.location.pathname.split('/')[1] === 'parts' && window.location.pathname.split('/')[2] !== 'type' && !window.location.pathname.split('/')[3]) {
                  return $(instructions).html('Enter the Part Name, Part Number, Part Amount, and Van Number: ').css('color', 'black');
                } else {
                  return $(instructions).html('Part Type: ' + '<b>' + window.location.pathname.split('/')[3] + '</b>').css('color', 'black');
                }
              };
              text = 'id=' + id + '&partName=' + partNameHtml + '&newPartAmount=' + partAmountHtml + '&partNumber=' + partNumberHtml + '&newVan=' + vanNumHtml()
              + '&newUnit=' + partUnitHtml;
              url = (window.location.pathname.split('/')[2] !== 'type' && window.location.pathname !== '/parts' && !window.location.pathname.split('/vans/')[1]) ? '/update/van/' : '/update/part/';
              let toggles = ['.deleteBtn', '.updateBtn'].toString();
              postRequest(url, text, toggles, null, $getPath, newInstructions());
            }
          }
        });
        // Cancel button implementation
        $('.main').off().on('click', '#cancelUpdateBtn'+id, function(){
          toggleElem(id);
          // Reset to original values
          if (!window.location.pathname.split('/')[2] && window.location.pathname !== '/parts') {
            selectVanElem.val(origVal(selectVanElem));
          } else {
            partName.val(origVal(partName));
            partNumber.val(origVal(partNumber));
            partAmount.val(origVal(partAmount));
            selectVanElem.val(vanNumOptVal);
            selectUnit.html() === 'None' ? selectUnitElem.attr('selected', 'Select Unit')
                : selectUnitElem.val(partUnitOptVal);
          }
          toggleProps('.deleteBtn', '.updateBtn');
        });
      });
    },
    confirmAccount : function ($getPath) {
      $('.main').off('click').on('click', '.confirmBtn', function() {
        let id = this.dataset.value;
        let confirmBtn = $('#confirmBtn' + id);
        let confirmText = $('#confirmText' + id);
        let confirmYesBtn = $('#confirmYesBtn' + id);
        let denyNoBtn = $('#denyNoBtn' + id);
        let denyBtn = $('#denyBtn' + id);
        let denyBtnCls = $('.denyBtn');
        let deleteBtnCls = $('.deleteBtn');
        let confirmBtnCls = $('.confirmBtn');
        let makeAdminBtn = $('.makeAdminBtn');
        toggleProps('.confirmBtn', denyBtnCls, deleteBtnCls, makeAdminBtn);
        toggleMe(confirmBtn, confirmText, confirmYesBtn, denyNoBtn, denyBtn);
        // Un-attach and re-attach the event listener
        $(confirmYesBtn).off('click').click(function () {
          // Parameters to be sent in the request
          let url = '/users';
          let data = 'user_id=' + id;
          let toggles = ['.confirmBtn', '.deleteBtn', '.denyBtn', '.makeAdminBtn'].toString();
          postRequest(url, data, toggles, null, $getPath);
        });
        $(denyNoBtn).off('click').click(function () {
          toggleProps(confirmBtnCls, denyBtnCls, deleteBtnCls, makeAdminBtn);
          toggleMe(confirmBtn, confirmText, confirmYesBtn, denyNoBtn, denyBtn);
        });
      });
    },
    denyAccount : function ($getPath) {
      $('table').off().on('click', '.denyBtn', function(){
        let id = this.dataset.value;
        let confirmBtn = $('#confirmBtn' + id);
        let confirmText = $('#confirmText' + id);
        let confirmYesBtn = $('#confirmYesBtn' + id);
        let denyNoBtn = $('#denyNoBtn' + id);
        let denyBtn = $('#denyBtn' + id);
        let denyBtnCls = $('.denyBtn');
        let confirmBtnCls = $('.confirmBtn');
        let deleteBtnCls = $('.deleteBtn');
        let makeAdminBtn = $('.makeAdminBtn');
        toggleProps(confirmBtnCls, denyBtnCls, deleteBtnCls, makeAdminBtn);
        toggleMe(confirmBtn, confirmText, confirmYesBtn, denyNoBtn, denyBtn);
        // Un-attach and re-attach the event listener
        $(confirmYesBtn).off('click').click(function () {
          // Parameters to be sent in the request
          let url = '/delete/user';
          let data = 'user_id=' + id;
          let toggles = ['.confirmBtn', '.denyBtn', '.deleteBtn', '.makeAdminBtn'].toString();
          postRequest(url, data, toggles, null, $getPath);
        });
        $('.denyNoBtn').off('click').on('click', denyNoBtn, function () {
          toggleProps(confirmBtnCls, denyBtnCls, deleteBtnCls, makeAdminBtn);
          toggleMe(confirmBtn, confirmText, confirmYesBtn, denyNoBtn, denyBtn);
        });
      });
    },
    deleteAccount : function ($getPath) {
      $(document.body).off('click').on('click', '.deleteBtn', function(){
        let id = this.dataset.value;
        let makeAdminBtn = $('#makeAdminBtn' + id);
        let adminBtnCls = $('.makeAdminBtn');
        let confirmText = $('#confirmNote' + id);
        let yesBtn = $('#thisYesBtn' + id);
        let noBtn = $('#thisNoBtn' + id);
        let deleteBtn = $('#deleteBtn' + id);
        toggleProps('.deleteBtn', '.denyBtn', '.confirmBtn', '.confirmYesBtn', '.denyNoBtn', adminBtnCls);
        toggleMe(deleteBtn, confirmText, yesBtn, noBtn, makeAdminBtn);
        // Un-attach and re-attach the event listener
        $(yesBtn).off().click(function () {
          // Parameters to be sent in the request
          let url = '/delete/user';
          let data = 'user_id=' + id;
          let toggles = ['.deleteBtn', '.denyBtn', '.confirmBtn', '.confirmYesBtn', '.denyNoBtn', '.makeAdminBtn'].toString();
          postRequest(url, data, toggles, null, $getPath);
        });
        $(noBtn).off('click').click(function () {
          toggleProps('.deleteBtn', '.denyBtn', '.confirmBtn', '.confirmYesBtn', '.denyNoBtn', adminBtnCls);
          toggleMe(deleteBtn, confirmText, yesBtn, noBtn, makeAdminBtn);
        });
      });
    },
    makeUserAdmin : function ($getPath) {
      $(document).off('click').on('click', '.makeAdminBtn', function(){
        let id = this.dataset.value;
        let makeAdminBtn = $('#makeAdminBtn' + id);
        let adminBtnCls = $('.makeAdminBtn');
        let confirmBtn = $('#confirmBtn' + id);
        let confirmText = $('#confirmNote' + id);
        let confirmYesBtn = $('#thisYesBtn' + id);
        let denyBtn = $('#thisNoBtn' + id);
        let deleteBtn = $('#deleteBtn' + id);
        let denyBtnCls = $('.denyBtn');
        let confirmBtnCls = $('.confirmBtn');
        let deleteBtnCls = $('.deleteBtn');
        toggleProps(confirmBtnCls, denyBtnCls, deleteBtnCls, adminBtnCls);
        toggleMe(confirmBtn, confirmText, confirmYesBtn, denyBtn, deleteBtn, makeAdminBtn);
        let is_admin = function() {
          let val;
          let returnVal;
          // Get if the user is admin or not, return opposite value
          $('#table #adminRow' + id).each(function() {
            val = $(this).html();
          });
          // If the cell value is Yes, return the opposite; otherwise return the opposite value from No (1)
          val === 'Yes' ? returnVal = 0 : returnVal = 1;
          return returnVal;
        }();
        // Un-attach and re-attach the event listener
        $(confirmYesBtn).off('click').click(function () {
          let url = '/update/user';
          let data = 'user_id=' + id + '&value=' + is_admin;
          let toggles = ['.confirmBtn', '.denyBtn', '.deleteBtn', '.makeAdminBtn'].toString();
          // Our POST request
          postRequest(url, data, toggles, null, $getPath);
        });
        $(denyBtn).off('click').click(function () {
          toggleProps(confirmBtnCls, denyBtnCls, deleteBtnCls, adminBtnCls);
          toggleMe(confirmBtn, confirmText, confirmYesBtn, denyBtn, deleteBtn, makeAdminBtn);
        });
      });
    },
    createJob : function (getPath) {
      let submitBtn = $('.submitJob');
      let toggles = ['.submitJob', '.resetValBtn'].toString();
      let instructions = $('#instructions');
      $(submitBtn).off().click(function () {
        let jsonData = function () {
          let jsonObj = [];
          $('input[class=changeAmount]').each(function() {
            let id = $(this).attr('data-value');
            let amount = $(this).val();
            let orig = $(this).attr('max');
            let item = {}
            item ['amount'] = amount;
            item ['part_id'] = id;
            // Make sure the values are not more than what exists in the database
            if (parseInt(amount) > parseInt(orig)) {
                $(instructions).html('Invalid input will not be accepted').css('color', 'red');
                jsonObj.push(null);
            } else {
                jsonObj.push(item);
            }
          });
          return JSON.stringify(jsonObj);
        }
        // If the values are correct, proceed
        if (!jsonData().includes('null')) {
          toggleProps(toggles);
          let url = '/jobs/' + window.location.pathname.split('/jobs/')[1];
        $.ajax({
          type: 'POST',
          url: url,
          data: jsonData(),
          contentType: 'application/json; charset=utf-8',
          cache: false,
          timeout: 800000,
          // On success, load the span from the getPath
          success: function () {
            $(instructions).html('Record a job in the database: ').css('color', 'black');
            $('#table').load(getPath);
            toggleProps(toggles);
          },
          // On failure, print errors
          error: function (e) {
            console.log('ERROR : ', e);
            toggleProps(toggles);
          }
        });
        }
      });
      // Reset value to default
      $(document).off('click').on('click', '.resetValBtn', function(){
        let partAmt = this.dataset.value;
        $('#changeAmount' + partAmt).prop('value', partAmt);
      });
    },
    // Functionality for the refresh button on /jobs
    refreshJobs : function (getPath) {
      let table = $('#table');
      let btn = $('.refreshJobs');
      $(btn).click(function () {
        $(table).load(getPath);
          $(btn).attr('disabled', true);
          $(btn).html('Please wait before refreshing again');
          setTimeout(function () {
            $(btn).attr('disabled', false);
            $(btn).html('Refresh');
          }, 5000);
      });
    },
    // Functionality to add part type on /parts/type
    addType : function (getPath) {
      let typeName = $('#typeName');
      let typeUnit = $('#typeUnit');
      let submitBtn = $('#submit');
      let instructions = $('#instructions');
      let form = $('#myForm');
      $(submitBtn).click(function (event) {
        event.preventDefault();
        if (typeName.val() && typeUnit.val()) {
          let url = '/parts/type';
          let data = 'typeName=' + typeName.val() + '&typeUnit=' + typeUnit.val();
          postRequest(url, data, submitBtn, null, getPath);
          toggleProps(submitBtn);
          $(form).trigger('reset');
          $(instructions).html('Enter a Part Type and a Part Unit ' +
              '(i.e. measure capacity in how many Feet, Parts, etc.):  ').css('color', 'black');
        } else {
          $(instructions).html('Invalid or blank input not allowed.').css('color', 'red');
          // Disable the submit button for 3 seconds after invalid input detected
          toggleProps(submitBtn);
          setTimeout(function () {
            toggleProps(submitBtn);
          }, 3000);
        }
      });
    },
    updateType : function(getPath) {
      $(document.body).off().on('click', '.updateBtn', function() {
        let id = this.dataset.value;
        let yesBtn = $('#confirmUpdateBtn' + id);
        let noBtn = $('#cancelUpdateBtn' + id);
        let newTypeName = $('#newTypeName' + id);
        let newTypeUnit = $('#newTypeUnit' + id);
        let typeUnit = $('#thisPartTypeUnit' + id);
        let typeName = $('#thisPartTypeName' + id);
        let updateBtn = $('#updateBtn' + id);
        let updateBtnCls = $('.updateBtn');
        let instructions = $('#instructions');
        let denyBtn = $('#deleteBtn' + id);
        let denyBtnCls = $('.denyBtn');
        let confirmBtnCls = $('.confirmBtn');
        let deleteBtnCls = $('.deleteBtn');
        toggleProps(confirmBtnCls, denyBtnCls, deleteBtnCls, updateBtnCls);
        toggleMe(yesBtn, noBtn, newTypeName, newTypeUnit, typeUnit, typeName, updateBtn, denyBtn);
        $(yesBtn).off().click(function () {
          if (newTypeName.val() && newTypeUnit.val()) {
            const url = '/update/type'
            let data = 'id=' + id + '&newTypeName=' + newTypeName.val() + '&newTypeUnit=' + newTypeUnit.val();
            let toggles = ['.confirmBtnCls', '.denyBtn', '.deleteBtn', '.updateBtn'].toString();
            postRequest(url, data, toggles, null, getPath, $(instructions).html('Enter a Part Type and a Part Unit ' +
                '(i.e. measure capacity in how many Feet, Parts, etc.):').css('color', 'black'), 'updateType');
          } else {
            $(instructions).html('Invalid or blank input not allowed').css('color', 'red');
          }
        });
        $(noBtn).off().click(function () {
          toggleProps(confirmBtnCls, denyBtnCls, deleteBtnCls, updateBtnCls);
          toggleMe(yesBtn, noBtn, newTypeName, newTypeUnit, typeUnit, typeName, updateBtn, denyBtn);
          newTypeName.val(origVal(newTypeName));
          newTypeUnit.val(origVal(newTypeUnit));
        });
      });
    },
    deleteType : function (getPath) {
      $(document).off().on('click', '.deleteBtn', function () {
        let id = this.dataset.value;
        let updateBtnCls = $('.updateBtn');
        let denyBtn = $('#deleteBtn' + id);
        let noBtn = $('#noBtn' + id);
        let denyBtnCls = $('.denyBtn');
        let confirmBtnCls = $('.confirmBtn');
        let deleteBtnCls = $('.deleteBtn');
        let submitBtn = $('#yesBtn' + id);
        let updateBtn = $('#updateBtn' + id);
        let confirmMe = $('#confirmMe' + id);
        toggleProps(confirmBtnCls, denyBtnCls, deleteBtnCls, updateBtnCls);
        toggleMe(confirmMe, updateBtn, denyBtn);
        $(submitBtn).click(function () {
          const url = '/delete/type';
          let data = 'id=' + id;
          let toggles = ['.confirmBtn', '.deleteBtn', '.denyBtn'].toString();
          postRequest(url, data, toggles, null, getPath, null, 'delete');
        });
        $(noBtn).off().click(function () {
          toggleProps(confirmBtnCls, denyBtnCls, deleteBtnCls, updateBtnCls);
          toggleMe(confirmMe, updateBtn, denyBtn);
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
          // Disable submit button until something happens
          $(btnLogin).prop('disabled', true);
          toggleInput('#username', '#password');
          $('html').css('cursor', 'progress');
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
              $(instructions).html('Login').css('color', 'black');
              $('html').css('cursor', 'default');
              location.reload();
            },
            // On failure, print errors and re-enable the submit button
            error: function (e) {
              $('html').css('cursor', 'default');
              $(btnLogin).prop('disabled', false);
              toggleInput('#username', '#password');
              // Reset the password if incorrect user/pass combo
              $('#password').val(null);
              if (e.status === 401) {
                $(instructions).html('Incorrect login credentials').css('color', 'red');
              } else {
                console.log('ERROR : ', e);
              }
              $(btnLogin).prop('disabled', false);
            }
          });
        }
      });
    },
    registerUser : function () {
      let registerBtn = $('#registerBtn');
      // On submit, execute the following
      $(registerBtn).click(function (event) {
        let username = $('#username');
        let password = $('#password');
        let confPass = $('#confPass');
        let instructions = $('#instructions');
        event.preventDefault();
        if (password.val() === confPass.val() && username.val() && password.val() && confPass.val()) {
          // Prevents form from submitting
          const form = $('#registerForm')[0];
          const data = new FormData(form);
          // Disable submit button until something happens
          $(registerBtn).prop('disabled', true);
          toggleInput('#username', '#password', '#confPass');
          $('html').css('cursor', 'progress');
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
              window.location.replace('/login');
              $('html').css('cursor', 'default');
            },
            // On failure, print errors and re-enable the submit button
            error: function (e) {
              $('html').css('cursor', 'default');
              toggleInput('#username', '#password', '#confPass');
              if (e.status === 409) {
                $(instructions).html('Username already exists, please try again').css('color', 'red');
                $('#username').val(null);
              } else {
                console.log('ERROR : ', e);
              }
              $(registerBtn).prop('disabled', false);
            }
          });
        } else if (password.val() !== confPass.val() || !password.val() || !confPass.val() || !username.val()) {
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