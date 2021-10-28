// This excerpt of code was provided by the Mozilla foundation:
// https://developer.mozilla.org/en-US/docs/Learn/Forms/Sending_forms_through_JavaScript
const getPath = '/table/main/all';

function sendData(content, dest) {
    const XHR = new XMLHttpRequest();

    // On a successful submission, it gets an AJAX request to refresh the contents of the table
    XHR.addEventListener("load", function() {
      htmx.ajax('GET', getPath, '#table');
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
window.addEventListener("load",function() {
    const form = document.getElementById("myForm");
  // Get the myForm element and assign it to a variable
  function sendMyData() {
    const XHR = new XMLHttpRequest();

    // Bind the FormData object and the form element
    const FD = new FormData(form);

    // On a successful submission, it gets an AJAX request to refresh the contents of the table
    XHR.addEventListener("load", function() {
      htmx.ajax('GET', getPath, '#table');
    });

    // Define what happens in case of error
    XHR.addEventListener("error", function() {
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
  form.addEventListener("submit", function (event) {
    event.preventDefault();
    sendMyData();
    form.reset();
  });
});

// Function that sends a POST request to /delete to delete a row entry by ID
function deleteMe(id) {
    if (window.confirm('Are you sure you want to delete?')) {
        // Parameters to be sent in the request
        const params = 'Delete=' + id;
        // Send our request
        sendData(params, '/delete/part/');
    }
}

// Function for sending a POST request to the /update route to update data entries by ID
function updateMe(id) {
  let text;
  let partName = prompt("Please enter the part name:", "PartName");
  let partNumber = prompt("Please enter the part number:", "PartNumber");
  let vanNumber = prompt("Please enter the van number:", "vanNumber");
  if (partName == null || partName === "" || partNumber == null || partNumber === "" || vanNumber == null || vanNumber === "" || isNaN(vanNumber)) {
      alert('Blank input will not be accepted.');
    } else {
      text = 'id=' + id + '&part_name=' + partName + '&part_number=' + partNumber + '&van_number=' + vanNumber;
    }
  // Send our request
  sendData(text, '/update');
}