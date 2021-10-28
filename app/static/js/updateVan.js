function updateTheData(content, dest) {
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
// Function for sending a POST request to the /update route to update data entries by ID
function updateVan(id) {
  let text;
  let vanNumber = prompt("Please enter the new van number:", "vanNumber");
  if (vanNumber == null || vanNumber === "") {
      alert('Blank input will not be accepted.');
    } else {
      text = 'id=' + id + '&van_number=' + vanNumber;
    }
  // Send our request
  updateTheData(text, '/update/van/');
}