$(document).ready(function(){
  const currentURL = (window.location.pathname);
  const getPath = '/table' + window.location.pathname;
  // Gets the number of the current van selected by the end of the pathname
  const vanNum = currentURL.split("/")[2];
  // On click, execute the following
  $('#table').on('click', '.updateMe', function(){
    // ID to be updated
    let id = this.dataset.value;
    let text;
    let partName = prompt("Please enter the part name:", "PartName");
    let partNumber = prompt("Please enter the part number:", "PartNumber");
    if (partName == null || partName === "" || partNumber == null || partNumber === "") {
      alert('Blank input will not be accepted.');
    } else {
      text = 'id=' + id + '&part_name=' + partName + '&part_number=' + partNumber + '&van_number=' + vanNum;
    }
    // Send our POST request
    $.ajax({
      url: '/update/part/',
      type: 'POST',
      data: text,
      success: function() {
        $("#table").load(getPath);
      }
    });
  });
});