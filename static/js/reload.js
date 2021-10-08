// This excerpt of code was provided by the Mozilla foundation:
// https://developer.mozilla.org/en-US/docs/Learn/Forms/Sending_forms_through_JavaScript
window.addEventListener("load",function() {
  // Get the myForm element and assign it to a variable
  const form = document.getElementById("myForm");
  function sendData() {
    const XHR = new XMLHttpRequest();

    // Bind the FormData object and the form element
    const FD = new FormData(form);

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
function myFunction(x) {
  x.classList.toggle("change");
}