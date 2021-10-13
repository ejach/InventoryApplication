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
    XHR.addEventListener("load", function() {
      htmx.ajax('GET', '/table', '#table');
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
    sendData();
  });
});

// Function that sends a POST request to /delete to delete a row entry by ID
function deleteMe(id) {
  // Parameters to be sent in the request
  const params = 'Delete=' + id;
  // Instantiate the XMLHTTP request
  const xhr = new XMLHttpRequest();
  // Open a POST request to /delete with async enabled
  xhr.open("POST", '/delete', true);

  // Send the proper header information along with the request
  xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

  // On a successful submission, it gets an AJAX request to refresh the contents of the table
  xhr.addEventListener("load", function() {
    htmx.ajax('GET', '/table', '#table');
  });

  // Send the parameters
  xhr.send(params);
}

// Function for sending a POST request to the /update route to update data entries by ID
function updateMe(id) {
  let text;
  let partName = prompt("Please enter the part name:", "PartName");
  let partNumber = prompt("Please enter the part number:", "PartNumber");
  if (partName == null || partName === "" && partNumber == null || partNumber === "") {
      alert('Blank input will not be accepted.');
    } else {
      text = 'id=' + id + '&part_name=' + partName + '&part_number=' + partNumber;
    }
  function sendData() {
    const XHR = new XMLHttpRequest();

    // On a successful submission, it gets an AJAX request to refresh the contents of the table
    XHR.addEventListener("load", function() {
      htmx.ajax('GET', '/table', '#table');
    });

    // Define what happens in case of error
    XHR.addEventListener("error", function() {
      console.log('POST request was not successful.');
    });

    // Set up our request
    XHR.open("POST","/update");

      // Send the proper header information along with the request
    XHR.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

    // The data sent is what the user provided in the form
    XHR.send(text);
  }
  // Send our request
  sendData();
}

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