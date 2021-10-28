function sendTheData(content, dest) {
    const getPath = '/table/vans_list/all';
    const XHR = new XMLHttpRequest();

    // On a successful submission, it gets an AJAX request to refresh the contents of the table
    XHR.addEventListener("load", function() {
      htmx.ajax('GET', getPath, '#mySpan');
    });

    // Define what happens in case of error
    XHR.addEventListener("error", function() {
      console.log('POST request was not successful.');
    });

    // Set up our request
    XHR.open("POST", dest);

      // Send the proper header information along with the request
    XHR.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

    // The data sent is what the user provided in the form
    XHR.send(content);
}

function deleteVan(id) {
    if (window.confirm('Are you sure you want to delete?')) {
        // Parameters to be sent in the request
        const params = 'Delete=' + id;
        // Send our request
        sendTheData(params, '/delete/van/');
    }
}