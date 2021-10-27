window.addEventListener("load",function() {
    const form = document.getElementById("formElement");
    const getPath = '/table/vans_list/all'
  // Get the myForm element and assign it to a variable
  function sendMyData() {
    const XHR = new XMLHttpRequest();

    // Bind the FormData object and the form element
    const FD = new FormData(form);

    // On a successful submission, it gets an AJAX request to refresh the contents of the table
    XHR.addEventListener("load", function() {
      htmx.ajax('GET', getPath, '#mySpan');
    });

    // Define what happens in case of error
    XHR.addEventListener("error", function() {
      console.log('POST request was not successful.');
    });

    // Set up our request
    XHR.open("POST","/vans");

    // The data sent is what the user provided in the form
    XHR.send(FD);

    // Reset the form
    form.reset()
  }
  // Replace the submit event with our sendData function
  form.addEventListener("submit", function (event) {
    event.preventDefault();
    sendMyData();
    form.reset();
  });
});