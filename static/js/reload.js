// This excerpt of code was provided by the Mozilla foundation:
// https://developer.mozilla.org/en-US/docs/Learn/Forms/Sending_forms_through_JavaScript
window.addEventListener("load",function() {
  // Get the myForm element and assign it to a variable
  const form = document.getElementById("myForm");
  function sendData() {
    const XHR = new XMLHttpRequest();

    // Bind the FormData object and the form element
    const FD = new FormData(form);

    // On a successful submission, it gets an AJAX request to refresh the contents of the table
    XHR.addEventListener( "load", function(event) {
      htmx.ajax('GET', '/table', '#table');
    } );

    // Define what happens in case of error
    XHR.addEventListener("error", function( event) {
      console.log('POST request was not successful.');
    });

    // Set up our request
    XHR.open("POST","/");

    // The data sent is what the user provided in the form
    XHR.send(FD);

    // Reset the form
    document.getElementById('myForm').reset()
  }

  // Replace the submit event with our sendData function
  form.addEventListener( "submit", function ( event ) {
    event.preventDefault();
    sendData();
  });
});


window.onload = function() {
  // Implementation to use the PullToRefresh library to perform an AJAX request to update the table
  const ptr = PullToRefresh.init({
      mainElement: 'body',
      onRefresh() {
        htmx.ajax('GET', '/table', '#table');
      }
    });
  // Implementation to make the 'hamburger' menu animation fire upon clicking
  document.getElementById("container").addEventListener("click", function() {
      let x = document.getElementById('container');
      x.classList.toggle("change");
  });
}