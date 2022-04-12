$(document).ready(function() {
    let instructions = $('#instructions');
    let partStoreName = $('#partStoreName');
    let partStoreImage = $('#partStoreImage');
    // Path to obtain the partStore list
    const getPath = '/table/part_store_list/all';
    // On submit, execute the following
    $('#btnSubmit').click(function (event) {
    // Prevents form from submitting
    event.preventDefault();
    $('html').css('cursor', 'progress');
    const form = $('#formElement')[0];
    const data = new FormData(form);
    if (partStoreName.val() && partStoreImage.val()) {
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
                $(instructions).html(instructions.data('value')).css('color', 'black');
                $('html').css('cursor', 'default');
            },
            // On failure, print errors and re-enable the submit button
            error: function (e) {
                if (e.status === 409) {
                    $('#instructions').html('Duplicate entries are not allowed.').css('color', 'red');
                } else {
                    console.log('ERROR : ', e);
                }
                $('#btnSubmit').prop('disabled', false);
                $('html').css('cursor', 'default');
            }
        });
        $(form).trigger('reset');
    } else {
        $('html').css('cursor', 'default');
        $(instructions).html('Invalid or blank input will not be accepted').css('color', 'red');
    }
  });
});