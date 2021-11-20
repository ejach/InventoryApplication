$(document).ready(function(){
  // Path to update van list
  const getPath = '/table/main/all';
  // On click, execute the following
  $('.main').on('click', '.updateBtn', function(){
    // ID to be updated
    let id = this.dataset.value;
    let text;
    let partName = prompt("Please enter the part name:", "PartName");
    let partNumber = prompt("Please enter the part number:", "PartNumber");
    let vanNumber = prompt("Please enter the van number:", "vanNumber");
    if (partName == null || partName === "" || partNumber == null || partNumber === "" || vanNumber == null || vanNumber === "") {
      alert('Blank input will not be accepted.');
    } else {
      text = 'id=' + id + '&part_name=' + partName + '&part_number=' + partNumber + '&van_number=' + vanNumber;
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